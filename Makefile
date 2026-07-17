RENPY_SDK ?=
JAVA_HOME ?=

ifeq ($(OS),Windows_NT)
RENPY_RUN = $(RENPY_SDK)/renpy.exe
PYTHON = python
else
RENPY_RUN = $(RENPY_SDK)/renpy.sh
PYTHON = python3
endif

ANDROID_SDK_ROOT ?= $(RENPY_SDK)/rapt/Sdk
ADB ?= adb

APP_PACKAGE ?= com.example.week_traveler

FLIT ?= $(PYTHON) -m flit

DIST_DIR = dist
WHL_FILES = $(wildcard $(DIST_DIR)/*.whl)
WRAPPER_FILE = wrapper.rpy
TESTS := $(patsubst tests/test_%,%,$(wildcard tests/test_*))

.PHONY: all build test test-% android-build android-run clean check-env generate_sound

all: build

check-env:
	@$(if $(strip $(RENPY_SDK)),,$(error Error: RENPY_SDK is not set. Please set it to your Ren'Py SDK directory.))
	@$(if $(strip $(JAVA_HOME)),,$(error Error: JAVA_HOME is not set. Please set it to your JDK installation directory.))

build: check-env
	$(FLIT) build --format wheel
	@echo "Wheel built: $(WHL_FILES)"

test: build $(patsubst %,test-%,$(TESTS))
	@echo "All requested tests finished."

test-%: build
	$(MAKE) _run_test DIR=tests/test_$*/ NAME=$*

_run_test:
	@echo "Testing $(NAME)"
	$(PYTHON) -c "import shutil, sys; from pathlib import Path; game_dir = Path(sys.argv[1]); dist_dir = Path(sys.argv[2]); wrapper_path = Path(sys.argv[3]); package_dir = game_dir / 'python-packages'; shutil.rmtree(package_dir, ignore_errors=True); package_dir.mkdir(parents=True, exist_ok=True); [shutil.copy2(wheel, package_dir / wheel.name) for wheel in dist_dir.glob('*.whl')]; shutil.copy2(wrapper_path, game_dir / wrapper_path.name)" "$(DIR)game" "$(DIST_DIR)" "$(CURDIR)/$(WRAPPER_FILE)"
	$(RENPY_RUN) "$(CURDIR)/$(DIR)game"

android-build: build
	@echo "Preparing week_traveler for Android..."
	$(PYTHON) -c "import shutil, sys; from pathlib import Path; sample_dir = Path('samples/week_traveler'); game_dir = sample_dir / 'game'; dist_dir = Path('dist'); wrapper_path = Path('wrapper.rpy'); package_dir = game_dir / 'python-packages'; shutil.rmtree(package_dir, ignore_errors=True); package_dir.mkdir(parents=True, exist_ok=True); [shutil.copy2(wheel, package_dir / wheel.name) for wheel in dist_dir.glob('*.whl')]; shutil.copy2(wrapper_path, game_dir / wrapper_path.name)"
	$(RENPY_RUN) android build "$(CURDIR)/samples/week_traveler" --destination "$(CURDIR)/out/apk/week_traveler"
	@echo "APK generated in out/apk/week_traveler/bin/"

android-run:
	$(PYTHON) -c "import os, subprocess, sys; from pathlib import Path; apk_dir = Path('out/apk/week_traveler/bin'); apks = sorted(apk_dir.glob('*.apk')); sys.exit(0) if apks else (print("No APK found - run 'make android-build' first."), sys.exit(1)); apk = apks[0]; adb = os.environ.get('ADB', 'adb'); subprocess.run([adb, 'install', '-r', str(apk)], check=True); subprocess.run([adb, 'shell', 'monkey', '-p', '$(APP_PACKAGE)', '-c', 'android.intent.category.LAUNCHER', '1'], check=True)"

clean:
	$(PYTHON) -c "import shutil; from pathlib import Path; shutil.rmtree('dist', ignore_errors=True); shutil.rmtree('out/apk', ignore_errors=True); [shutil.rmtree(path, ignore_errors=True) for path in Path('tests').glob('**/python-packages')]; [Path(path).unlink(missing_ok=True) for path in Path('tests').glob('**/wrapper.rpy')]; [shutil.rmtree(path, ignore_errors=True) for path in Path('samples').glob('**/python-packages')]; [Path(path).unlink(missing_ok=True) for path in Path('samples').glob('**/wrapper.rpy')]"
	@echo "All build artifacts and temporary copies removed."

generate_sound: generate_sound_venv
ifeq ($(OS),Windows_NT)
	generate_sound_venv\Scripts\pip.exe install -r sound_requirements.txt
	generate_sound_venv\Scripts\python.exe -m generate_sound
else
	./generate_sound_venv/bin/pip install -r sound_requirements.txt
	./generate_sound_venv/bin/python -m generate_sound
endif

generate_sound_venv:
	$(PYTHON) -m venv generate_sound_venv

