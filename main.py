import os
import sys
import subprocess
import tempfile
import shutil

# مسیر Ezsynth را به sys.path اضافه کن (چون به صورت پکیج نصب نمی‌شود)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EZSYNTH_PATH = os.path.join(BASE_DIR, 'ezsynth_lib')
if os.path.exists(EZSYNTH_PATH):
    sys.path.insert(0, EZSYNTH_PATH)

from ezsynth.main_ez import Ezsynth
from ezsynth.aux_classes import RunConfig
from ezsynth.aux_utils import save_seq

def extract_frames(video_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    cmd = ['ffmpeg', '-i', video_path, os.path.join(output_dir, 'frame_%06d.png')]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def frames_to_video(frames_dir, output_video, fps=30):
    cmd = ['ffmpeg', '-framerate', str(fps), '-i', os.path.join(frames_dir, '%06d.png'),
           '-c:v', 'libx264', '-pix_fmt', 'yuv420p', output_video]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run_conversion(input_video, output_video, style_image=None, fps=30):
    """تبدیل ویدیو به انیمیشن با Ezsynth و مدل سبک EF_RAFT"""
    with tempfile.TemporaryDirectory() as tmpdir:
        frames_dir = os.path.join(tmpdir, 'frames')
        extract_frames(input_video, frames_dir)
        frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])
        if not frame_files:
            raise RuntimeError("هیچ فریمی استخراج نشد. آیا ffmpeg نصب است؟")

        # اگر تصویر استایل داده نشده، از فریم اول استفاده کن
        if style_image is None:
            style_image = os.path.join(frames_dir, frame_files[0])

        # تنظیمات Ezsynth با مدل سبک EF_RAFT
        cfg = RunConfig(pre_mask=False, feather=5)
        ez = Ezsynth(
            style_paths=[style_image],
            image_folder=frames_dir,
            cfg=cfg,
            edge_method="PAGE",               # روش لبه‌یابی خوب و نسبتاً سریع
            raft_flow_model_name="25000_ours-sintel",  # مدل سبک EF_RAFT
            do_mask=False,
            flow_arch="EF_RAFT"              # سبک‌ترین معماری جریان نوری
        )

        # اجرای استایل‌دهی
        stylized_frames, _, _ = ez.run_sequences_full(only_mode=None, return_flow=True)

        # ذخیره فریم‌های استایل‌شده در پوشه موقت
        stylized_dir = os.path.join(tmpdir, 'stylized')
        os.makedirs(stylized_dir, exist_ok=True)
        save_seq(stylized_frames, stylized_dir)

        # تبدیل فریم‌ها به ویدیوی خروجی
        frames_to_video(stylized_dir, output_video, fps=fps)

if __name__ == '__main__':
    # اگر آرگومان خط فرمان وجود داشت، حالت CLI
    if len(sys.argv) > 1:
        import argparse
        parser = argparse.ArgumentParser(description='تبدیل ویدیو به انیمیشن با Ezsynth (EF_RAFT)')
        parser.add_argument('input', help='مسیر ویدیوی ورودی')
        parser.add_argument('output', help='مسیر ویدیوی خروجی')
        parser.add_argument('--style', help='تصویر استایل (اختیاری)')
        parser.add_argument('--fps', type=int, default=30, help='نرخ فریم خروجی')
        args = parser.parse_args()
        run_conversion(args.input, args.output, args.style, args.fps)
    else:
        # حالت گرافیکی ساده با Tkinter
        import tkinter as tk
        from tkinter import filedialog, messagebox

        root = tk.Tk()
        root.title("Video to Anime (Ezsynth Offline)")
        root.geometry("500x250")

        input_var = tk.StringVar()
        output_var = tk.StringVar()

        def select_input():
            path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
            if path:
                input_var.set(path)

        def select_output():
            path = filedialog.asksaveasfilename(defaultextension=".mp4",
                                                filetypes=[("MP4 video", "*.mp4")])
            if path:
                output_var.set(path)

        def start():
            if not input_var.get() or not output_var.get():
                messagebox.showerror("خطا", "لطفاً ورودی و خروجی را انتخاب کنید.")
                return
            try:
                start_btn.config(state='disabled')
                run_conversion(input_var.get(), output_var.get())
                messagebox.showinfo("موفق", "تبدیل با موفقیت انجام شد!")
            except Exception as e:
                messagebox.showerror("خطا", str(e))
            finally:
                start_btn.config(state='normal')

        tk.Label(root, text="ویدیوی ورودی:").pack(pady=5)
        tk.Entry(root, textvariable=input_var, width=50).pack()
        tk.Button(root, text="انتخاب فایل", command=select_input).pack(pady=5)

        tk.Label(root, text="فایل خروجی:").pack(pady=5)
        tk.Entry(root, textvariable=output_var, width=50).pack()
        tk.Button(root, text="انتخاب مسیر", command=select_output).pack(pady=5)

        start_btn = tk.Button(root, text="شروع تبدیل", command=start, bg="green", fg="white")
        start_btn.pack(pady=10)

        root.mainloop()
