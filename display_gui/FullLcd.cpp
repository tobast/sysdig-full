#include "FullLcd.h"

FullLcd::FullLcd()
{
    buildWidget();
    setRenderHints(QPainter::Antialiasing | QPainter::SmoothPixmapTransform);
}

void FullLcd::setDigit(int digitPos, unsigned char digitVal)
{
    digits[digitPos]->setSegments(digitVal);
}

void FullLcd::buildWidget()
{
    for(int i=0; i < 14; i++)
        digits.push_back(new DigitalNumber);
    scene.setBackgroundBrush(QBrush(Qt::black));

    static const int DIGIT_WIDTH = DigitalNumber::digitWidth(),
            DIGITS_SEP_WIDTH = 10,
            MARGIN = 10;

    // ========== ADD 7-segments to the scene =================
    int widShift = MARGIN, heiShift = MARGIN;

    // ---- DAY ----
    digits[0]->setPos(widShift, heiShift);
    widShift += DIGIT_WIDTH + DIGITS_SEP_WIDTH;
    scene.addItem(digits[0]);
    digits[1]->setPos(widShift, heiShift);
    widShift += DIGIT_WIDTH + DIGITS_SEP_WIDTH;
    scene.addItem(digits[1]);

    scene.addItem(makeDateSeparator(widShift, heiShift, widShift));

    // ---- MONTH ----
    digits[2]->setPos(widShift, heiShift);
    widShift += DIGIT_WIDTH + DIGITS_SEP_WIDTH;
    scene.addItem(digits[2]);
    digits[3]->setPos(widShift, heiShift);
    widShift += DIGIT_WIDTH + DIGITS_SEP_WIDTH;
    scene.addItem(digits[3]);

    scene.addItem(makeDateSeparator(widShift, heiShift, widShift));

    // ---- YEAR ----
    digits[4]->setPos(widShift, heiShift);
    widShift += DIGIT_WIDTH + DIGITS_SEP_WIDTH;
    scene.addItem(digits[4]);
    digits[5]->setPos(widShift, heiShift);
    widShift += DIGIT_WIDTH + DIGITS_SEP_WIDTH;
    scene.addItem(digits[5]);
    digits[6]->setPos(widShift, heiShift);
    widShift += DIGIT_WIDTH + DIGITS_SEP_WIDTH;
    scene.addItem(digits[6]);
    digits[7]->setPos(widShift, heiShift);
    widShift += DIGIT_WIDTH + DIGITS_SEP_WIDTH;
    scene.addItem(digits[7]);

    widShift = MARGIN + DIGIT_WIDTH + DIGITS_SEP_WIDTH;
    heiShift += DigitalNumber::digitHeight() + 2*MARGIN;

    // ---- HOUR ----
    digits[8]->setPos(widShift, heiShift);
    widShift += DIGIT_WIDTH + DIGITS_SEP_WIDTH;
    scene.addItem(digits[8]);
    digits[9]->setPos(widShift, heiShift);
    widShift += DIGIT_WIDTH + DIGITS_SEP_WIDTH;
    scene.addItem(digits[9]);

    scene.addItem(makeColon(widShift, heiShift, widShift));

    // ---- MINUTE ----
    digits[10]->setPos(widShift, heiShift);
    widShift += DIGIT_WIDTH + DIGITS_SEP_WIDTH;
    scene.addItem(digits[10]);
    digits[11]->setPos(widShift, heiShift);
    widShift += DIGIT_WIDTH + DIGITS_SEP_WIDTH;
    scene.addItem(digits[11]);

    scene.addItem(makeColon(widShift, heiShift, widShift));

    // ---- SECOND ----
    digits[12]->setPos(widShift, heiShift);
    widShift += DIGIT_WIDTH + DIGITS_SEP_WIDTH;
    scene.addItem(digits[12]);
    digits[13]->setPos(widShift, heiShift);
    widShift += DIGIT_WIDTH + DIGITS_SEP_WIDTH;
    scene.addItem(digits[13]);


    // ========== FINISHED adding 7-segments  =================

    scene.setSceneRect(0,0,scene.width()+2*MARGIN, scene.height()+2*MARGIN);
    setScene(&scene);
}

QGraphicsItem *FullLcd::makeDateSeparator(int x, int y, int &shift)
{
    //DASH
    QGraphicsLineItem* out=new QGraphicsLineItem(
            0., ((double)DigitalNumber::digitHeight()) / 2.,
            DigitalNumber::digitWidth()/4,
            ((double)DigitalNumber::digitHeight()) / 2.);

    QPen pen(QColor(0xff,0,0),10, Qt::SolidLine, Qt::RoundCap);
    out->setPen(pen);
    out->setPos(x+10,y);
    shift += 10 + DigitalNumber::digitWidth()/4 + 20;
    return out;
}

QGraphicsItem *FullLcd::makeColon(int x, int y, int &shift)
{
    QGraphicsItemGroup* out = new QGraphicsItemGroup;
    QBrush brush(QColor(0xff,0,0));

    static const int HEIGHT = DigitalNumber::digitHeight();

    QGraphicsEllipseItem* upDot=new QGraphicsEllipseItem(
            0, HEIGHT/3 - 5, 10, 10);
    upDot->setBrush(brush);
    out->addToGroup(upDot);

    QGraphicsEllipseItem* downDot=new QGraphicsEllipseItem(
                0, 2*HEIGHT/3 - 5, 10,10);
    downDot->setBrush(brush);
    out->addToGroup(downDot);

    out->setPos(x+10,y);
    shift += 10 + 20;
    return out;
}

