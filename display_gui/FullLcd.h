#ifndef FULLLCD_H
#define FULLLCD_H

#include <QBrush>
#include <QColor>
#include <QGraphicsView>
#include <QGraphicsScene>
#include <QGraphicsItemGroup>

#include <vector>

#include "DigitalNumber.h"

class FullLcd : public QGraphicsView
{
public:
    FullLcd();
    void setDigit(int digitPos, unsigned char digitVal);

private: // meth
    void buildWidget();
    QGraphicsItem* makeDateSeparator(int x, int y, int& shift);
    QGraphicsItem* makeColon(int x, int y, int& shift);

private:
    std::vector<DigitalNumber*> digits;
    // In this order (ie. digits[0] is the first D):
    // DDMMYYYYHHMMSS

    QGraphicsScene scene;
};

#endif // FULLLCD_H
