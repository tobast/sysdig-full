#ifndef STDINREADER_H
#define STDINREADER_H

#include <QObject>

#include <QList>
#include <cstdio>

typedef unsigned char* StdinResult;

class StdinReader : public QObject
{
    Q_OBJECT
public:
    explicit StdinReader(QObject *parent = 0);

signals:
    void hasResult(StdinResult);

public slots:
    void flush();
    void getResult();
};

#endif // STDINREADER_H
