#include "StdinReader.h"


StdinReader::StdinReader(QObject *parent) : QObject(parent)
{
    qRegisterMetaType<StdinResult>("StdinResult");
}

void StdinReader::flush()
{
    fflush(stdin);
}

void StdinReader::getResult()
{
    unsigned char out[16];
    //out.resize(16);
    for(int i=0; i < 16; i++) {
        do {
            scanf("%c", &(out[i]));
        } while(out[i] == '\n');
    }
    emit hasResult(out);
}
