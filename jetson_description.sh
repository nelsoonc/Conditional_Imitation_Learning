#!/bin/bash
# Script: acquire basic information from your Jetson device
# author: nelsoonc
# Bandung Institute of Technology, Mechanical Engineering 2017

if [ -f /sys/module/tegra_fuse/parameters/tegra_chip_id ]; then
    case $(cat /sys/module/tegra_fuse/parameters/tegra_chip_id) in
        64)
            JETSON_BOARD="TK1" ;;
        33)
            JETSON_BOARD="TX1" ;;
        24)
            JETSON_BOARD="TX2" ;;
        25)
            JETSON_BOARD="AGX Xavier"
        *)
            JETSON_BOARD="UNKNOWN" ;;
    esac
    JETSON_DESCRIPTION="NVIDIA Jetson $JETSON_BOARD"
fi

if [ -f /etc/nv_tegra_release ]; then
    # L4T string
    JETSON_L4T_STRING=$(cat /etc/nv_tegra_release)

    # Load release and revision
    JETSON_L4T_RELEASE=$(echo $JETSON_L4T_STRING | cut -f1 -d ',' | sed 's/[^0-9]//g')
    JETSON_L4T_REVISION=$(echo $JETSON_L4T_STRING | cut -f2 -d ',' | sed 's/[^0-9.]//g' )
    # unset variable
    unset JETSON_L4T_STRING
    
    # Write Jetson description
    JETSON_L4T="$JETSON_L4T_RELEASE.$JETSON_L4T_REVISION"

    # Write version of jetpack installed
    # https://developer.nvidia.com/embedded/jetpack-archive
    if [ "$JETSON_BOARD" = "TX2i" ] ; then 
        case $JETSON_L4T in
            "28.2.1")
                JETSON_JETPACK="3.2.1" ;;
            "28.2") 
               JETSON_JETPACK="3.2" ;;
            *)
               JETSON_JETPACK="UNKNOWN" ;;
        esac        
    elif [ "$JETSON_BOARD" = "TX2" ] ; then
        case $JETSON_L4T in
            "32.6.1")
                JETSON_JETPACK="4.6" ;;
            "32.5.1")
                JETSON_JETPACK="4.5.1" ;;
            "32.5")
                JETSON_JETPACK="4.5" ;;
            "32.4.4")
                JETSON_JETPACK="4.4.1"
            "32.4.3")
                JETSON_JETPACK="4.4"
            "28.2.1")
                JETSON_JETPACK="3.2.1" ;;
            "28.2") 
                JETSON_JETPACK="3.2" ;;
            "28.1") 
                JETSON_JETPACK="3.1" ;;
            "27.1") 
                JETSON_JETPACK="3.0" ;;
            *)
                JETSON_JETPACK="UNKNOWN" ;;
        esac
    elif [ "$JETSON_BOARD" = "TX1" ] ; then
        case $JETSON_L4T in
            "28.2") 
                JETSON_JETPACK="3.2 or 3.2.1" ;;
            "28.1") 
                JETSON_JETPACK="3.1" ;;
            "24.2.1") 
                JETSON_JETPACK="3.0 or 2.3.1" ;;
            "24.2") 
                JETSON_JETPACK="2.3" ;;
            "24.1") 
                JETSON_JETPACK="2.2.1 or 2.2" ;;
            "23.2") 
                JETSON_JETPACK="2.1" ;;
            "23.1") 
                JETSON_JETPACK="2.0" ;;
            *)
                JETSON_JETPACK="UNKNOWN" ;;
        esac
    elif [ "$JETSON_BOARD" ="TK1" ] ; then
        case $JETSON_L4T in
            "21.5") 
                JETSON_JETPACK="2.3.1 or 2.3" ;;
            "21.4") 
                JETSON_JETPACK="2.2 or 2.1 or 2.0 or DP 1.2" ;;
            "21.3") 
                JETSON_JETPACK="DP 1.1" ;;
            "21.2") 
                JETSON_JETPACK="DP 1.0" ;;
            *)
                JETSON_JETPACK="UNKNOWN" ;;
        esac
    else
        # Unknown board
        JETSON_JETPACK="UNKNOWN"
    fi
fi

# Read CUDA version
if [ -f /usr/local/cuda/version.txt ]; then
    JETSON_CUDA=$(cat /usr/local/cuda/version.txt | sed 's/CUDA Version //g')
else
    JETSON_CUDA="NOT INSTALLED"
fi

export JETSON_BOARD
export JETSON_L4T
export JETSON_JETPACK
export JETSON_CUDA