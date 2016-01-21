/*
 * Shamelessly stolen from my (Théophile Bastian) own previous project,
 * RubiksTimer (https://github.com/tobast/rubiks_timer)
 */

#include "DigitalNumber.h"


DigitalNumber::DigitalNumber()
{
    segOffPen = QPen(QColor(0x1A,0,0));
    //segOffPen = QPen(QColor(0x53,0,0));
	segOffPen.setWidth(SEG_WIDTH/2);
	segOffPen.setCapStyle(Qt::RoundCap);
	segOnPen = QPen(segOffPen);
	segOnPen.setColor(QColor(0xff,0,0));

	buildWidget();
    setSegments(0u);
}

void DigitalNumber::setSegments(unsigned char matrix)
{
	for(size_t seg=0; seg<segments.size(); ++seg)
        segments[seg]->setPen(((matrix & (1<<seg)) != 0) ? segOnPen : segOffPen);
}

void DigitalNumber::buildWidget()
{
	segments.push_back(new QGraphicsLineItem(SEG_WIDTH*1.5f, SEG_WIDTH*0.5f,
			SEG_WIDTH*1.5+SEG_HEIGHT, SEG_WIDTH*0.5f));
	segments.push_back(new QGraphicsLineItem(SEG_WIDTH*2.5f+SEG_HEIGHT,
			SEG_WIDTH*1.5f, SEG_WIDTH*2.5+SEG_HEIGHT,
			SEG_WIDTH*1.5f+SEG_HEIGHT));
	segments.push_back(new QGraphicsLineItem(SEG_WIDTH*2.5f+SEG_HEIGHT,
			SEG_WIDTH*3.5f+SEG_HEIGHT, SEG_WIDTH*2.5+SEG_HEIGHT,
			SEG_WIDTH*3.5f+2*SEG_HEIGHT));
	segments.push_back(new QGraphicsLineItem(SEG_WIDTH*1.5f,
			SEG_WIDTH*4.5f+2*SEG_HEIGHT, SEG_WIDTH*1.5+SEG_HEIGHT,
			SEG_WIDTH*4.5f+2*SEG_HEIGHT));
	segments.push_back(new QGraphicsLineItem(SEG_WIDTH*0.5f,
			SEG_WIDTH*3.5f+SEG_HEIGHT, SEG_WIDTH*0.5,
			SEG_WIDTH*3.5f+2*SEG_HEIGHT));
	segments.push_back(new QGraphicsLineItem(SEG_WIDTH*0.5f, SEG_WIDTH*1.5f,
			SEG_WIDTH*0.5, SEG_WIDTH*1.5f+SEG_HEIGHT));
	segments.push_back(new QGraphicsLineItem(SEG_WIDTH*1.5f,
			SEG_WIDTH*2.5f+SEG_HEIGHT, SEG_WIDTH*1.5+SEG_HEIGHT,
			SEG_WIDTH*2.5f+SEG_HEIGHT));

	for(size_t seg=0; seg<segments.size(); ++seg)
    {
		segments[seg]->setPen(segOffPen);
		addToGroup(segments[seg]);
	}
}

