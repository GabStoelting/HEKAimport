/********************************************************************************
** Form generated from reading UI file 'HEKATree.ui'
**
** Created by: Qt User Interface Compiler version 5.6.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef HEKATREE_H
#define HEKATREE_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QDialog>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QTreeView>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_Dialog
{
public:
    QTreeView *treeView;
    QPushButton *displayButton;
    QWidget *widget;
    QPushButton *openButton;
    QPushButton *saveButton;

    void setupUi(QDialog *Dialog)
    {
        if (Dialog->objectName().isEmpty())
            Dialog->setObjectName(QStringLiteral("Dialog"));
        Dialog->resize(1098, 640);
        treeView = new QTreeView(Dialog);
        treeView->setObjectName(QStringLiteral("treeView"));
        treeView->setGeometry(QRect(10, 30, 256, 281));
        displayButton = new QPushButton(Dialog);
        displayButton->setObjectName(QStringLiteral("displayButton"));
        displayButton->setGeometry(QRect(150, 320, 111, 41));
        widget = new QWidget(Dialog);
        widget->setObjectName(QStringLiteral("widget"));
        widget->setGeometry(QRect(279, 9, 801, 621));
        openButton = new QPushButton(Dialog);
        openButton->setObjectName(QStringLiteral("openButton"));
        openButton->setGeometry(QRect(10, 320, 111, 41));
        saveButton = new QPushButton(Dialog);
        saveButton->setObjectName(QStringLiteral("saveButton"));
        saveButton->setGeometry(QRect(150, 370, 111, 41));

        retranslateUi(Dialog);

        QMetaObject::connectSlotsByName(Dialog);
    } // setupUi

    void retranslateUi(QDialog *Dialog)
    {
        Dialog->setWindowTitle(QApplication::translate("Dialog", "HEKA to Python", 0));
        displayButton->setText(QApplication::translate("Dialog", "Display", 0));
        openButton->setText(QApplication::translate("Dialog", "Open File...", 0));
        saveButton->setText(QApplication::translate("Dialog", "Save as .csv...", 0));
    } // retranslateUi

};

namespace Ui {
    class Dialog: public Ui_Dialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // HEKATREE_H
