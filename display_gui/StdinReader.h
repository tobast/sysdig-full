#ifndef STDINREADER_H
#define STDINREADER_H

#include <QObject>

#include <QList>
#include <QTimer>
#include <cstdio>

typedef unsigned char* StdinResult;

class StdinReader : public QObject
{
    Q_OBJECT
public:
    explicit StdinReader(QObject *parent = 0);
    ~StdinReader();

signals:
    void hasResult(StdinResult);
    void nextUpdate();

public slots:
    void flush();
    void getResult();
private slots:
    void update();

private:
    unsigned char* buffer, *sharedBuffer;
    bool resultRequested;
};

#endif // STDINREADER_H
