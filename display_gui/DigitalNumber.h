/*
 * Shamelessly stolen from my (Théophile Bastian) own previous project,
 * RubiksTimer (https://github.com/tobast/rubiks_timer)
 */

#ifndef DEF_DIGITALNUMBER
#define DEF_DIGITALNUMBER

#include <QGraphicsItemGroup>
#include <QGraphicsLineItem>
#include <QBrush>
#include <QPen>
#include <vector>

/* Digits are represented by a boolean matrix describing the state of each segment as following :
 *  _a_
 * f   b
 * |_g_|
 * e   c
 * |_d_|
 *
 * where the matrix is an unsigned char, its least significant bit being a and its (most significant - 1) being g
 */

#ifndef SCALEFACT
#define SCALEFACT 1.
#endif

static const int SEG_HEIGHT=SCALEFACT*50, SEG_WIDTH=SCALEFACT*10;
class DigitalNumber : public QGraphicsItemGroup
{
	public:
        DigitalNumber();
        void setSegments(unsigned char matrix);
		static int digitWidth() { return (3*SEG_WIDTH+SEG_HEIGHT); }
		static int digitHeight() { return (5*SEG_WIDTH+2*SEG_HEIGHT); }

	private: //meth
		void buildWidget();

	private:
		QPen segOffPen, segOnPen;
		std::vector<QGraphicsLineItem*> segments;
};

#endif//DEF_DIGITALNUMBER

