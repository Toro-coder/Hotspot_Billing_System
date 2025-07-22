import React, { createContext, useContext, useState, useCallback } from "react";

const AlertContext = createContext();

export const useAlert = () => useContext(AlertContext);

export const AlertProvider = ({ children }) => {
  const [alert, setAlert] = useState(null);

  const showAlert = useCallback((message, duration = 4000) => {
    setAlert({ message, duration });
  }, []);

  return (
    <AlertContext.Provider value={showAlert}>
      {children}
      {alert && <TimedAlert {...alert} onClose={() => setAlert(null)} />}
    </AlertContext.Provider>
  );
};

// Reusable alert component with animation and auto-close
const TimedAlert = ({ message, duration, onClose }) => {
  const [progress, setProgress] = useState(100);

  React.useEffect(() => {
    const interval = 100;
    const step = 100 / (duration / interval);
    const timer = setInterval(() => {
      setProgress(prev => {
        if (prev <= 0) {
          clearInterval(timer);
          onClose();
          return 0;
        }
        return prev - step;
      });
    }, interval);
    return () => clearInterval(timer);
  }, [duration, onClose]);

  return (
    <div className="fixed top-5 min-w-36 justify-self-center bg-white border border-red-500 shadow-md rounded-xl p-4 z-50">
      <p className="text-red-700 font-bold text-base md:text-lg">{message}</p>
      <div className="mt-2 h-1 bg-red-100 rounded overflow-hidden">
        <div
          className="h-full bg-red-500 transition-all duration-100"
          style={{ width: `${progress}%` }}
        ></div>
      </div>
    </div>
  );
};
