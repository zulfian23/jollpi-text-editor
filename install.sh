#!/bin/bash
# Installer
# Copyright (c) 2010 Zulfian
# license : GPL

app_name='jollpi'
dist=`lsb_release -i -s`

if [ -z "$1" ];then
	echo "[01;33mUsage : $0 OPSI[0m"
	echo "[01;33mOPSI :[0m"
	echo "[01;33m    -i   to install jollpi[0m"
	echo "[01;33m    -u   to uninstall jollpi[0m"
	exit 1
fi

function install_jollpi(){
	echo "[01;33mChecking for dependencies[0m"
	echo "[01;33mPlease wait...[0m"
	echo ""
	echo -n "Checking for python..."
	
	PYTHON=`which python`
	if [ $PYTHON ];then
		echo "[01;32m  OK[0m"
	else
		echo "[01;31m  not found ![0m"
		echo "[01;31mPlease install python.[0m"
		exit 1
	fi
	
	echo -n "Checking for python-gtk..."
	
	python -c "import pygtk, gtk"
	GTK=$?
	if [ $GTK -eq 0 ];then
		echo "[01;32m  OK[0m"
	else
		echo "[01;31m  not found ![0m"
		echo "[01;31mPlease install python-gtk[0m"
		exit 1
	fi
	
	echo -n "Checking for python-gtksourceview2..."
	python -c "import gtksourceview2"
	GTKS=$?
	if [ $GTKS -eq 0 ];then
		echo "[01;32m  OK[0m"
	else
		echo "[01;31m  not found ![0m"
		echo "[01;31mPlease install python-gtksourceview2[0m"
		exit 1
	fi
	
	echo -n "Checking for pango..."
	python -c "import pango"
	PANGO=$?
	if [ $PANGO -eq 0 ];then
		echo "[01;32m  OK[0m"
	else
		echo "[01;31m  not found ![0m"
		echo "[01;31mPlease install pango[0m"
		exit 1
	fi
	
	echo -n "Checking for python-gobject..."
	python -c "import gobject"
	GOBJECT=$?
	if [ $GOBJECT -eq 0 ];then
		echo "[01;32m  OK[0m"
		echo -n "Checking for gio..."
		python -c "import gio"
		GIO=$?
		if [ $GIO -eq 0 ];then
			echo "[01;32m  OK[0m"
		else
			echo "[01;31m  not found ![0m"
			echo -n "Checking for gnomevfs..."
			python -c "import gnomevfs"
			GNOMEVFS=$?
			if [ $GNOMEVFS -eq 0 ];then
				echo "[01;32m  OK[0m"
			else
				echo "[01;31m  not found ![0m"
				echo "[01;31mPlease install gnomevfs[0m"
				exit 1
			fi
		fi
	else
		echo "[01;31m  not found ![0m"
		echo "[01;31mPlease install python-gobject[0m"
		exit 1
	fi
	
	echo -n "Checking for evince..."
	EVINCE=`which evince`
	if [ $EVINCE ];then
		echo "[01;32m  OK[0m"
	else
		echo "[01;31m  not found ![0m"
		echo "[01;31mPlease install evince later[0m"
	fi

	echo "[01;33mInstalling Jollpi[0m"
	mkdir -p $PWD/$app_name/docs
	cp LICENSE ChangeLog $PWD/$app_name/docs
	if [ $dist == "Ubuntu" ];then
		sudo su -c "python setup.py install"
	else
		su -c "python setup.py install"
	fi

	if [ "$?" == 0 ];then
		echo "[01;33mJollpi successfully installed[0m"
	else
		echo "[01;31mAborted ![0m"
		echo "[01;31mJollpi is not installed ![0m"
		echo "[01;31mTry again ![0m"
	fi
	rm -rf $PWD/$app_name/docs
}

function remove_jollpi(){
	sitepack=`python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`
	DIR1="/usr"
	DIR2="/usr/local"
	if [ -x "$DIR1/bin/$app_name" ];then
		if [ $dist == "Ubuntu" ];then
			sudo su -c "rm -r $DIR1/bin/$app_name;rm -rf $sitepack/$app_name;rm -rf $DIR1/share/doc/$app_name;rm -r $DIR1/share/applications/$app_name.desktop"
		else
			su -c "rm -r $DIR1/bin/$app_name;rm -rf $sitepack/$app_name;rm -rf $DIR1/share/doc/$app_name;rm -r $DIR1/share/applications/$app_name.desktop"
		fi
	else
		if [ $dist == "Ubuntu" ];then
			sudo su -c "rm -r $DIR2/bin/$app_name;rm -rf $sitepack/$app_name;rm -rf $DIR2/share/doc/$app_name;rm -r $DIR2/share/applications/$app_name.desktop"
		else
			su -c "rm -r $DIR2/bin/$app_name;rm -rf $sitepack/$app_name;rm -rf $DIR2/share/doc/$app_name;rm -r $DIR2/share/applications/$app_name.desktop"
		fi
	fi
	
	if [ "$?" == 0 ];then
		echo "[01;33mJollpi successfully uninstalled[0m"
	else
		echo "[01;31mAborted ![0m"
		echo "[01;31mJollpi is not uninstalled ![0m"
		echo "[01;31mTry again ![0m"
	fi
}

if [ "$1" = "-i" ];then
	path=`which jollpi`
	if [ $path ];then
		echo "[01;32mJollpi is already installed[0m"
	else
		install_jollpi
	fi
elif [ "$1" = "-u" ];then
	path=`which jollpi`
	if [ $path ];then
		echo -n "[01;33mDo you want to uninstall Jollpi ? [y/N] :[0m"
		read answer1
		if [ "$answer1" == "y" ];then
			remove_jollpi
		else
			echo "[01;32mJollpi not uninstalled[0m"
		fi
	else
		echo "[01;32mJollpi has not been installed[0m"
	fi
fi
