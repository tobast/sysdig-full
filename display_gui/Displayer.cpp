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

    QTimer::singleShot(0, stdinReader, SLOT(getResult()));
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
    QTime time;
    time.start();

    for(int pos=2; pos < 8; pos++) // Time
        lcd->setDigit(6+pos, res[pos]);
    for(int pos=8; pos < 12; pos++) // Year
        lcd->setDigit(pos-4, res[pos]);
    lcd->setDigit(0, res[14]); // Day_0
    lcd->setDigit(1, res[15]); // Day_1

    lcd->setDigit(2, res[12]); // Month_0
    lcd->setDigit(3, res[13]); // Month_1

    stdinReader->flush();

    int elapsed = time.elapsed();
    if(elapsed < 17) // 60 FPS
        QTimer::singleShot(17-elapsed, this, SIGNAL(requestValues()));
    else
        emit requestValues();
}
