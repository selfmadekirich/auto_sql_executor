import addNotification from "react-push-notification";

function successNotification( title, message) {
        addNotification({
            title: title,
            message: message,
            theme: "light",
            closeButton: "X",
            backgroundTop: "#10b981",
            duration: 5000
        });
    }

function errorNotification(message) {
      addNotification({
          title: "Ошибка!",
          message: message,
          theme: "red",
          closeButton: "X",
      });
  }

export {successNotification, errorNotification}