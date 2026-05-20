import QtQuick
import "Theme.js" as Theme

Rectangle {
    id: root

    property bool active: false
    property alias text: label.text

    signal clicked()

    implicitHeight: Theme.chipHeight
    radius: 4
    color: active ? Theme.accent : "transparent"
    border.color: active ? Theme.accent : Theme.chipBorder
    border.width: 1

    Text {
        id: label
        anchors.centerIn: parent
        font.pixelSize: Theme.fontSm
        color: root.active ? Theme.accentText : Theme.chipText
    }

    MouseArea {
        anchors.fill: parent
        onClicked: root.clicked()
    }
}
