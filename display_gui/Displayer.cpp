#include "Displayer.h"

Displayer::Displayer(QWidget *parent) :
    QWidget(parent)
{
    buildWidget();

    readerThread = new QThread;
    stdinReader = new StdinReader;
    stdinReader->moveToThread(readerThread);

    connect(stdinReader, SIGNAL(hasResult(StdinResult)),
            this, SLOT(updateLCD(StdinResult)));
    connect(this, SIGNAL(requestValues()), stdinReader, SLOT(getResult()));
    readerThread->start();
    stdinReader->getResult();
}

Displayer::~Displayer()
{
    readerThread->quit();
    stdinReader->deleteLater();
}

void Displayer::buildWidget()
{
    l_main = new QVBoxLayout;

    lcd = new FullLcd;
    l_main->addWidget(lcd);

    setLayout(l_main);
}

void Displayer::updateLCD(StdinResult res)
{
    for(int pos=2; pos < 8; pos++) // Time
        lcd->setDigit(6+pos, res[pos]);
    for(int pos=8; pos < 12; pos++) // Year
        lcd->setDigit(pos-4, res[pos]);
    lcd->setDigit(0, res[14]); // Day_0
    lcd->setDigit(1, res[15]); // Day_1

    lcd->setDigit(2, res[12]); // Month_0
    lcd->setDigit(3, res[13]); // Month_1

    stdinReader->flush();
    emit requestValues();
}
