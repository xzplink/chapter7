#!/bin/bash
# Create by zhaozhang@yxlink.com
# On 2017/03/20

WORK_DIR="/root/virt"
if [ $# -eq 2 ]; then
    WORK_DIR=$1
fi

TARGET_DIR="/root/latest_bin"
CGI_BIN_DIR="${WORK_DIR}/build-cgi-project-Desktop_Qt_5_8_0_GCC_64bit-Debug"
VIRT_BIN_DIR="${WORK_DIR}/cgi-project/build-virt_bin-Desktop_Qt_5_8_0_GCC_64bit-Debug"
VIRT_LIB_DIR="${WORK_DIR}/cgi-project/build-virtmanager-Desktop_Qt_5_8_0_GCC_64bit-Debug"

echo ""
echo ""
if [ -d ${WORK_DIR} ] || exit 0

if [ ! -d ${TARGET_DIR} ]; then
    mkdir -p ${TARGET_DIR}
    mkdir -p ${TARGET_DIR}/cgi
    mkdir -p ${TARGET_DIR}/lib
fi

# 1、Install cgi
install ${CGI_BIN_DIR}/* ${TARGET_DIR}/cgi

# 2、Install virt_bin
install ${VIRT_BIN_DIR}/virt_bin ${TARGET_DIR}

# 3、Install virt_lib
install ${VIRT_LIB_DIR}/*.so* ${TARGET_DIR}/lib

exit 0