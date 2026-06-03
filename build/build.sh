#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="${SRC_DIR:-/src}"
OUT_DIR="${OUT_DIR:-/out}"
WORK_DIR="${WORK_DIR:-/work}"
TARGETARCH="${TARGETARCH:-$(dpkg --print-architecture)}"
BUILD_ROOT="${WORK_DIR}/project"
PKG_DIR="${BUILD_ROOT}/deb_package"

rm -rf "${BUILD_ROOT}"
mkdir -p "${BUILD_ROOT}" "${OUT_DIR}"
cp -a "${SRC_DIR}/." "${BUILD_ROOT}/"

cd "${BUILD_ROOT}"

pyinstaller --onefile \
	--name nms-sm-evb_tests \
	--paths="${BUILD_ROOT}/src" \
	"${BUILD_ROOT}/src/main.py"

mkdir -p "${PKG_DIR}/DEBIAN" \
		 "${PKG_DIR}/usr/bin" \
		 "${PKG_DIR}/etc"

cp "${BUILD_ROOT}/dist/nms-sm-evb_tests" "${PKG_DIR}/usr/bin/"
cp "${BUILD_ROOT}/debian/control" "${PKG_DIR}/DEBIAN/"

DEB_ARCH="${TARGETARCH}"
if [ "${TARGETARCH}" = "arm" ]; then
	DEB_ARCH="armhf"
fi

sed -i "s/^Architecture: .*/Architecture: ${DEB_ARCH}/" "${PKG_DIR}/DEBIAN/control"

DEB_PATH="${BUILD_ROOT}/nms-sm-evb_tests_${DEB_ARCH}.deb"
dpkg-deb --build "${PKG_DIR}" "${DEB_PATH}"

cp "${DEB_PATH}" "${OUT_DIR}/"
cp "${BUILD_ROOT}/dist/nms-sm-evb_tests" "${OUT_DIR}/"

echo "Build completed. Artifacts are in ${OUT_DIR}"