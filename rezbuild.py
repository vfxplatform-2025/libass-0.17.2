# -*- coding: utf-8 -*-
import os
import sys
import shutil
import subprocess

def run_cmd(cmd, cwd=None):
    print(f"[RUN] {cmd}")
    subprocess.run(cmd, shell=True, check=True, cwd=cwd)

def clean_build_dir(build_path):
    if os.path.exists(build_path):
        print(f"🧹 Cleaning build directory: {build_path}")
        for item in os.listdir(build_path):
            item_path = os.path.join(build_path, item)
            if os.path.isfile(item_path) and item.endswith(".rxt"):
                continue
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)

def clean_install_dir(install_path):
    if os.path.exists(install_path):
        print(f"🧹 Removing install directory: {install_path}")
        shutil.rmtree(install_path)

def ensure_source(version, source_path):
    src_dir = os.path.join(source_path, "source", f"libass-{version}")
    if not os.path.exists(src_dir):
        print(f"🔁 Source missing. Running get_source.sh...")
        run_cmd("bash get_source.sh", cwd=source_path)
    else:
        print(f"✅ Source exists: {src_dir}")

def copy_package_py(source_path, install_path):
    src_pkg = os.path.join(source_path, "package.py")
    dst_pkg = os.path.join(install_path, "package.py")
    if os.path.exists(src_pkg):
        print(f"📄 Copying package.py → {dst_pkg}")
        shutil.copy(src_pkg, dst_pkg)

def build(source_path, build_path, install_path, targets):
    version = os.environ.get("REZ_BUILD_PROJECT_VERSION", "0.17.1")
    src_dir = os.path.join(source_path, "source", f"libass-{version}")

    clean_build_dir(build_path)
    if "install" in targets:
        install_path = f"/core/Linux/APPZ/packages/libass/{version}"
        clean_install_dir(install_path)

    ensure_source(version, source_path)

    os.makedirs(build_path, exist_ok=True)
    os.chdir(src_dir)

    # Configure
    run_cmd(f"./autogen.sh")
    run_cmd(f"./configure --prefix={install_path}")

    # Build
    run_cmd("make -j$(nproc)")

    if "install" in targets:
        run_cmd("make install")
        copy_package_py(source_path, install_path)

    print("✅ libass build completed.")

if __name__ == "__main__":
    build(
        source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
        build_path=os.environ["REZ_BUILD_PATH"],
        install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
        targets=sys.argv[1:]
    )

