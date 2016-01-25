#-------------------------------------------------
#
# Project created by QtCreator 2016-01-20T14:24:10
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = display_gui
TEMPLATE = app

QMAKE_CXXFLAGS += -DSCALEFACT=1.5

SOURCES += main.cpp\
        Displayer.cpp \
    DigitalNumber.cpp \
    FullLcd.cpp \
    StdinReader.cpp

HEADERS  += Displayer.h \
    DigitalNumber.h \
    FullLcd.h \
    StdinReader.h

FORMS    +=
