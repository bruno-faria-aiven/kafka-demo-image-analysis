#!/bin/bash

APP_NAME="streamlit_kafka_producer.py"  # Replace with the actual name of your Streamlit app
LOG_FILE="streamlit_producer.log"     # Log file for the output
PID_FILE="streamlit_producer.pid"     # File to store the process ID (PID)

case "$1" in
    start)
        if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
            echo "Streamlit producer is already running with PID $(cat $PID_FILE)."
        else
            echo "Starting Streamlit producer app..."
            nohup streamlit run $APP_NAME > $LOG_FILE 2>&1 &
            echo $! > "$PID_FILE"
            echo "Streamlit producer started with PID $(cat $PID_FILE)."
            sleep 1
            URL=$(cat $LOG_FILE | grep 'Local URL' | sed 's/^[ \t]*//')
            echo "Producer $URL"
        fi
        ;;
    
    stop)
        if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
            echo "Stopping Streamlit producer app with PID $(cat $PID_FILE)..."
            kill $(cat "$PID_FILE")
            rm "$PID_FILE"
            echo "Streamlit producer stopped."
        else
            echo "Streamlit producer is not running."
        fi
        ;;

    restart)
        $0 stop
        sleep 1
        $0 start
        ;;

    status)
        if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
            echo ""
            echo "Streamlit producer is running with PID $(cat $PID_FILE)."
            URL=$(cat $LOG_FILE | grep 'Local URL' | sed 's/^[ \t]*//')
            echo "Producer $URL"
            echo ""
        else
            echo "Streamlit producer is not running."
        fi
        ;;

    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

