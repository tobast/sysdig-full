#include "Displayer.h"

Displayer::Displayer(QWidget *parent) :
    QWidget(parent)
{
    buildWidget();
}

Displayer::~Displayer()
{
}

void Displayer::buildWidget()
{
    l_main = new QVBoxLayout;

    lcd = new FullLcd;
    l_main->addWidget(lcd);

    setLayout(l_main);
}
