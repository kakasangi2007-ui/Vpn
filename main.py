import sys
import os

# --- راه‌حل قطعی خطای tqdm در حالت بدون کنسول (PyInstaller --noconsole) ---
if getattr(sys, 'frozen', False) and sys.stdout is None:
    class DummyStream:
        def write(self, *args, **kwargs): pass
        def flush(self): pass
    sys.stdout = DummyStream()
    sys.stderr = DummyStream()

import time
import threading
import subprocess
import tempfile
import traceback

# ---------- مسیر پایه ----------
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FFMPEG_EXE = os.path.join(BASE_DIR, 'ffmpeg', 'ffmpeg.exe')
if not os.path.isfile(FFMPEG_EXE):
    FFMPEG_EXE = 'ffmpeg'  # fallback به PATH سیستم

EZSYNTH_PATH = os.path.join(BASE_DIR, 'ezsynth_lib')
if os.path.exists(EZSYNTH_PATH) and EZSYNTH_PATH not in sys.path:
    sys.path.insert(0, EZSYNTH_PATH)

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# ---------- تلاش برای import Ezsynth با پیام خطای واضح ----------
try:
    from ezsynth.main_ez import Ezsynth
    from ezsynth.aux_classes import RunConfig
    from ezsynth.aux_utils import save_seq
except Exception as e:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "خطای حیاتی",
        f"کتابخانه Ezsynth بارگذاری نشد:\n{e}\n\n"
        "مطمئن شوید پوشه ezsynth_lib در کنار برنامه وجود دارد."
    )
    sys.exit(1)


# ==================== توابع پردازش ====================

def _check_ffmpeg():
    global FFMPEG_EXE
    if os.path.isfile(FFMPEG_EXE):
        return FFMPEG_EXE
    import shutil
    found = shutil.which('ffmpeg')
    if found:
        FFMPEG_EXE = found
        return found
    raise FileNotFoundError(
        "ffmpeg پیدا نشد. لطفاً ffmpeg را در PATH سیستم قرار دهید "
        "یا فایل ffmpeg.exe را در پوشه ffmpeg کنار برنامه بگذارید."
    )


def extract_frames(video_path, output_dir):
    ffmpeg = _check_ffmpeg()
    os.makedirs(output_dir, exist_ok=True)
    cmd = [ffmpeg, '-i', video_path, os.path.join(output_dir, 'frame_%06d.png')]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        raise RuntimeError(
            "استخراج فریم‌ها با ffmpeg شکست خورد. "
            "آیا فایل ویدیو سالم است؟ فرمت آن پشتیبانی می‌شود؟"
        )


def frames_to_video(frames_dir, output_video, fps=30):
    ffmpeg = _check_ffmpeg()
    cmd = [
        ffmpeg, '-y',
        '-framerate', str(fps),
        '-i', os.path.join(frames_dir, '%06d.png'),
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        output_video
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        raise RuntimeError(
            "ساخت ویدیوی خروجی شکست خورد. "
            "احتمالاً فریم‌های ذخیره‌شده ناقص هستند."
        )


def _safe_unpack_ezsynth_result(result):
    if result is None:
        raise RuntimeError("Ezsynth مقدار None برگرداند. احتمالاً مدل‌های EF_RAFT وجود ندارند.")
    if isinstance(result, tuple):
        if len(result) == 0:
            raise RuntimeError("Ezsynth تاپل خالی برگرداند.")
        stylized = result[0]
    else:
        stylized = result

    if stylized is None:
        raise RuntimeError("لیست فریم‌های استایل‌شده None است.")
    if not hasattr(stylized, '__len__') or len(stylized) == 0:
        raise RuntimeError("Ezsynth هیچ فریمی تولید نکرد.")
    return stylized


def _fallback_save_frames(frames, out_dir):
    import numpy as np
    from PIL import Image
    os.makedirs(out_dir, exist_ok=True)
    for i, frame in enumerate(frames):
        if frame is None:
            continue
        if isinstance(frame, np.ndarray):
            if frame.dtype != np.uint8:
                frame = frame.astype('uint8')
            img = Image.fromarray(frame)
        else:
            img = frame
        img.save(os.path.join(out_dir, f'{i:06d}.png'))


def run_conversion(input_video, output_video, style_image=None, log_cb=None):
    t_start = time.time()

    def _log(msg):
        if log_cb:
            log_cb(msg)

    with tempfile.TemporaryDirectory() as tmpdir:
        frames_dir = os.path.join(tmpdir, 'frames')
        _log("استخراج فریم‌ها از ویدیو...")
        extract_frames(input_video, frames_dir)
        frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])
        if not frame_files:
            raise RuntimeError("هیچ فریمی استخراج نشد. ویدیو ممکن است خالی باشد.")
        total = len(frame_files)
        _log(f"مجموع فریم‌ها: {total}")

        if style_image is None:
            style_image = os.path.join(frames_dir, frame_files[0])

        cfg = RunConfig(pre_mask=False, feather=5)
        try:
            ez = Ezsynth(
                style_paths=[style_image],
                image_folder=frames_dir,
                cfg=cfg,
                edge_method="Classic",  # <--- تغییر یافت: استفاده از Classic به جای PAGE برای سازگاری با CPU
                raft_flow_model_name="25000_ours-sintel",
                do_mask=False,
                flow_arch="EF_RAFT",
            )
        except Exception as e:
            raise RuntimeError(f"راه‌اندازی Ezsynth شکست خورد: {e}")

        _log("در حال استایل‌دهی فریم‌ها... (ممکن است چند دقیقه طول بکشد)")
        start_style = time.time()
        try:
            result = ez.run_sequences_full(only_mode=None, return_flow=True)
        except Exception as e:
            raise RuntimeError(f"اجرای Ezsynth با خطا مواجه شد: {e}")
        elapsed_style = time.time() - start_style
        _log(f"استایل‌دهی تمام شد ({elapsed_style:.1f} ثانیه)")

        stylized_frames = _safe_unpack_ezsynth_result(result)
        _log(f"تعداد فریم‌های استایل‌شده: {len(stylized_frames)}")

        stylized_dir = os.path.join(tmpdir, 'stylized')
        os.makedirs(stylized_dir, exist_ok=True)
        _log("ذخیره فریم‌های استایل‌شده...")

        try:
            save_seq(stylized_frames, stylized_dir)
            if not any(f.endswith('.png') for f in os.listdir(stylized_dir)):
                raise RuntimeError("save_seq هیچ فایلی ذخیره نکرد.")
        except Exception as e:
            _log(f"save_seq شکست خورد ({e})، ذخیره دستی فریم‌ها...")
            _fallback_save_frames(stylized_frames, stylized_dir)

        if not any(f.endswith('.png') for f in os.listdir(stylized_dir)):
            raise RuntimeError("هیچ فریمی ذخیره نشد. پردازش ناقص است.")

        _log("ساخت ویدیوی خروجی...")
        frames_to_video(stylized_dir, output_video, fps=30)

        total_elapsed = time.time() - t_start
        _log(f"✅ تمام شد در {total_elapsed:.1f} ثانیه")


# ==================== رابط گرافیکی ====================

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Video to Anime — Ezsynth Offline")
        self.root.geometry("720x520")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(True, True)

        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
        except Exception:
            pass
        self.style.configure('TFrame', background='#1e1e2e')
        self.style.configure('TLabel', background='#1e1e2e', foreground='#cdd6f4', font=('Segoe UI', 10))
        self.style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), foreground='#89b4fa')
        self.style.configure('TButton', font=('Segoe UI', 10), padding=6)
        self.style.configure('Accent.TButton', background='#89b4fa', foreground='#1e1e2e', font=('Segoe UI', 11, 'bold'))
        self.style.map('Accent.TButton', background=[('active', '#74c7ec')])
        self.style.configure('TEntry', fieldbackground='#313244', foreground='#cdd6f4')

        self.input_var = tk.StringVar()
        self.output_var = tk.StringVar()
        self.status_var = tk.StringVar(value="آماده")
        self.frames_var = tk.StringVar(value="فریم‌ها: —")
        self.time_var = tk.StringVar(value="زمان سپری‌شده: —")

        self._build_ui()

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=20)
        main.pack(fill='both', expand=True)

        ttk.Label(main, text="🎬 Video to Anime", style='Title.TLabel').pack(anchor='w', pady=(0, 15))

        row1 = ttk.Frame(main); row1.pack(fill='x', pady=4)
        ttk.Label(row1, text="ویدیوی ورودی:", width=14).pack(side='left')
        ttk.Entry(row1, textvariable=self.input_var).pack(side='left', fill='x', expand=True, padx=5)
        ttk.Button(row1, text="انتخاب", command=self.select_input).pack(side='left')

        row2 = ttk.Frame(main); row2.pack(fill='x', pady=4)
        ttk.Label(row2, text="فایل خروجی:", width=14).pack(side='left')
        ttk.Entry(row2, textvariable=self.output_var).pack(side='left', fill='x', expand=True, padx=5)
        ttk.Button(row2, text="انتخاب", command=self.select_output).pack(side='left')

        self.start_btn = ttk.Button(main, text="🚀 شروع تبدیل", style='Accent.TButton', command=self.start)
        self.start_btn.pack(pady=15, ipadx=20, ipady=4)

        info = ttk.Frame(main); info.pack(fill='x', pady=4)
        ttk.Label(info, textvariable=self.status_var).pack(side='left')
        ttk.Label(info, textvariable=self.frames_var).pack(side='right')

        info2 = ttk.Frame(main); info2.pack(fill='x', pady=4)
        ttk.Label(info2, textvariable=self.time_var).pack(side='left')

        ttk.Label(main, text="گزارش:").pack(anchor='w', pady=(10, 2))
        self.log_text = tk.Text(main, height=12, bg='#11111b', fg='#cdd6f4',
                                insertbackground='#cdd6f4', relief='flat', wrap='word')
        self.log_text.pack(fill='both', expand=True)

    def select_input(self):
        path = filedialog.askopenfilename(filetypes=[("Video", "*.mp4 *.avi *.mov *.mkv")])
        if path:
            self.input_var.set(path)

    def select_output(self):
        path = filedialog.asksaveasfilename(defaultextension=".mp4",
                                            filetypes=[("MP4", "*.mp4")])
        if path:
            self.output_var.set(path)

    def log(self, msg):
        self.log_text.insert('end', msg + '\n')
        self.log_text.see('end')
        self.root.update_idletasks()

    @staticmethod
    def _fmt(sec):
        sec = int(sec)
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        if h:
            return f"{h}:{m:02d}:{s:02d}"
        return f"{m}:{s:02d}"

    def start(self):
        if not self.input_var.get() or not self.output_var.get():
            messagebox.showerror("خطا", "لطفاً ورودی و خروجی را انتخاب کنید.")
            return

        self.start_btn.config(state='disabled')
        self.log_text.delete('1.0', 'end')
        self.log("شروع فرایند...")
        self.status_var.set("در حال اجرا...")
        self.frames_var.set("فریم‌ها: —")
        self.time_var.set("زمان سپری‌شده: —")

        t = threading.Thread(target=self._worker, daemon=True)
        t.start()

    def _worker(self):
        try:
            t_start = time.time()

            def _log(msg):
                self.root.after(0, self.log, msg)
                elapsed = time.time() - t_start
                self.root.after(0, self.time_var.set, f"زمان سپری‌شده: {self._fmt(elapsed)}")
                if "مجموع فریم‌ها:" in msg:
                    try:
                        n = msg.split(":")[-1].strip()
                        self.root.after(0, self.frames_var.set, f"فریم‌ها: 0 / {n}")
                    except Exception:
                        pass
                if "استایل‌دهی تمام شد" in msg:
                    self.root.after(0, self.status_var.set, "در حال ساخت ویدیو...")

            run_conversion(
                self.input_var.get(),
                self.output_var.get(),
                log_cb=_log,
            )
            self.root.after(0, self._done, True, None)
        except Exception as e:
            tb = traceback.format_exc()
            self.root.after(0, self._done, False, f"{e}\n\n{tb}")

    def _done(self, ok, err):
        self.start_btn.config(state='normal')
        elapsed = self.time_var.get().replace("زمان سپری‌شده: ", "")
        if ok:
            self.status_var.set("✅ تمام شد")
            self.log("✅ تبدیل با موفقیت انجام شد.")
            messagebox.showinfo("موفق", f"تبدیل با موفقیت انجام شد!\nزمان کل: {elapsed}")
        else:
            self.status_var.set("❌ خطا")
            self.log(f"❌ خطا: {err}")
            messagebox.showerror("خطا", err)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
