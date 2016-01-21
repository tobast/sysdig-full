#ifndef DISPLAYER_H
#define DISPLAYER_H

#include <QVBoxLayout>
#include <QWidget>
#include <QThread>

#include "FullLcd.h"
#include "StdinReader.h"

class Displayer : public QWidget
{
    Q_OBJECT

public:
    explicit Displayer(QWidget *parent = 0);
    ~Displayer();

private: //meth
    void buildWidget();

private slots:
    void updateLCD(StdinResult res);
private:
    QVBoxLayout* l_main;
    FullLcd* lcd;

    StdinReader* stdinReader;
    QThread* readerThread;


signals:
    void requestValues();
};

#endif // DISPLAYER_H
