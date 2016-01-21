#include "StdinReader.h"


StdinReader::StdinReader(QObject *parent) :
    QObject(parent), resultRequested(false)
{
    qRegisterMetaType<StdinResult>("StdinResult");
    buffer = new unsigned char[16];
    sharedBuffer = new unsigned char[16];
    connect(this, SIGNAL(nextUpdate()), this, SLOT(update()));
    QTimer::singleShot(0, this, SLOT(update()));
}

StdinReader::~StdinReader()
{
    delete[] buffer;
    delete[] sharedBuffer;
}

void StdinReader::flush()
{
    // @DEPRECATED
}

void StdinReader::getResult()
{
    resultRequested = true;
}

void StdinReader::update()
{
    for(int i=0; i < 16 * 7; i++) // ignore 6 cycles out of 7
        buffer[i & 0xf] = getchar();
    if(resultRequested) {
        //unsigned char out[16]; // Copying to avoid problems of shared memory
        // (Remember, this is running in a separated thread)
        for(int i=0; i < 16; i++)
            sharedBuffer[i] = buffer[i];
        resultRequested = false;
        emit hasResult(sharedBuffer);
    }
    QTimer::singleShot(0, this, SLOT(update()));
}
