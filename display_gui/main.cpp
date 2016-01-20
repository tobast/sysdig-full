#include "Displayer.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    Displayer w;
    w.show();

    return a.exec();
}
