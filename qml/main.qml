import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "Theme.js" as Theme

ApplicationWindow {
    id: root
    visibility: Window.Maximized
    minimumWidth: 800
    minimumHeight: 500
    title: "ESO Addons Updater"
    color: Theme.bg

    palette.window:          Theme.bg
    palette.windowText:      Theme.textPrimary
    palette.base:            Theme.bgSurface
    palette.alternateBase:   "#2a2a2a"
    palette.text:            Theme.textPrimary
    palette.button:          "#2a2a2a"
    palette.buttonText:      Theme.textPrimary
    palette.highlight:       Theme.accent
    palette.highlightedText: Theme.accentText
    palette.placeholderText: Theme.textMuted
    palette.mid:             Theme.separator
    palette.dark:            "#333333"
    palette.light:           Theme.separator

    ColumnLayout {
        anchors.fill: parent
        spacing: 1
        enabled: updateOverlay.status === ""

        Rectangle {
            Layout.fillWidth: true
            height: 40
            color: Theme.bg

            TabBar {
                id: tabBar
                anchors.fill: parent
                contentHeight: 40
                currentIndex: 1

                TabButton {
                    text: "Catalogue"
                    font.pixelSize: Theme.fontLg
                    implicitWidth: 140
                }
                TabButton {
                    text: "Installed"
                    font.pixelSize: Theme.fontLg
                    implicitWidth: 140
                }
                TabButton {
                    text: "Exclusions"
                    font.pixelSize: Theme.fontLg
                    implicitWidth: 140
                }
                TabButton {
                    text: "Log"
                    font.pixelSize: Theme.fontLg
                    implicitWidth: 140
                }
            }
        }

        StackLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            currentIndex: tabBar.currentIndex

            AddonsTab {}
            InstalledTab {}
            ExclusionsTab {}
            LogTab {}
        }

        Rectangle {
            Layout.fillWidth: true
            height: 40
            color: Theme.bgSurface

            RowLayout {
                anchors { fill: parent; leftMargin: 12; rightMargin: 12 }
                spacing: 6

                Text {
                    text: "AddOns folder:"
                    font.pixelSize: Theme.fontMd
                    color: Theme.textSecondary
                }

                TextField {
                    id: targetDirField
                    Layout.preferredWidth: Math.max(120, dirMetrics.width + leftPadding + rightPadding + 8)
                    implicitHeight: 28
                    font.pixelSize: Theme.fontMd
                    text: backend ? backend.getTargetDirectory() : ""
                    placeholderText: "Path to AddOns folder..."
                    readOnly: true

                    TextMetrics {
                        id: dirMetrics
                        font: targetDirField.font
                        text: targetDirField.text
                    }
                }

                Button {
                    text: "..."
                    implicitWidth: 28
                    implicitHeight: 28
                    font.pixelSize: Theme.fontLg
                    onClicked: backend.browseTargetDirectory()
                }

                Item { Layout.fillWidth: true }

                Button {
                    text: "Launch TTC Client"
                    implicitHeight: Theme.buttonHeight
                    visible: ttcClientVisible
                    onClicked: backend.launchTtcClient()
                }

                Item { Layout.fillWidth: true }

                CheckBox {
                    text: "Sync on launch"
                    font.pixelSize: Theme.fontBase
                    checked: backend ? backend.getSyncOnLaunch() : false
                    onCheckedChanged: if (backend) backend.setSyncOnLaunch(checked)
                }

                Text {
                    text: "Syncing..."
                    font.pixelSize: Theme.fontBase
                    color: Theme.textSecondary
                    visible: syncIndicator.running
                }

                BusyIndicator {
                    id: syncIndicator
                    running: false
                    visible: running
                    Layout.preferredWidth: 28
                    Layout.preferredHeight: 28
                }

                Button {
                    text: "Sync"
                    visible: !syncIndicator.running
                    implicitHeight: Theme.buttonHeight
                    Layout.leftMargin: 4
                    onClicked: { tabBar.currentIndex = 3; backend.fetchAddonList(); backend.runUpdate() }
                }
            }
        }
    }

    Rectangle {
        id: updateOverlay
        anchors.fill: parent
        color: Theme.bg
        visible: status !== ""

        property string status: "Checking for updates..."
        property bool done: status.startsWith("Update complete")

        Column {
            anchors.centerIn: parent
            spacing: 16

            BusyIndicator {
                anchors.horizontalCenter: parent.horizontalCenter
                visible: !updateOverlay.done
            }

            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                text: "✓"
                color: "#4caf50"
                font.pixelSize: 48
                visible: updateOverlay.done
            }

            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                text: updateOverlay.status
                color: Theme.textPrimary
                font.pixelSize: 15
            }
        }

    }

    Connections {
        target: backend
        function onUpdateStarted()  { syncIndicator.running = true }
        function onUpdateFinished() { syncIndicator.running = false; ttcClientVisible = backend.hasTtcClient() }
        function onTargetDirectoryChanged(path) { targetDirField.text = path }
        function onAppUpdateStatus(msg) {
            updateOverlay.status = msg
            if (msg === "" && backend.getSyncOnLaunch()) {
                tabBar.currentIndex = 3
                backend.fetchAddonList()
                backend.runUpdate()
            }
        }
    }

    property bool ttcClientVisible: backend ? backend.hasTtcClient() : false

    Component.onCompleted: backend.checkForUpdate()
}
