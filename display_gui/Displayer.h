#ifndef DISPLAYER_H
#define DISPLAYER_H

#include <QVBoxLayout>
#include <QWidget>

#include "FullLcd.h"

class Displayer : public QWidget
{
    Q_OBJECT

public:
    explicit Displayer(QWidget *parent = 0);
    ~Displayer();

private: //meth
    void buildWidget();
private:
    QVBoxLayout* l_main;
    FullLcd* lcd;
};

#endif // DISPLAYER_H
