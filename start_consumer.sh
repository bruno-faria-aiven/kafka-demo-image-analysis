#!/bin/bash

APP_NAME="streamlit_kafka_consumer.py"  # Replace with the actual name of your Streamlit app
LOG_FILE="streamlit_consumer.log"     # Log file for the output
PID_FILE="streamlit_consumer.pid"     # File to store the process ID (PID)

case "$1" in
    start)
        if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
            echo "Streamlit consumer is already running with PID $(cat $PID_FILE)."
        else
            echo "Starting Streamlit consumer app..."
            nohup streamlit run $APP_NAME > $LOG_FILE 2>&1 &
            echo $! > "$PID_FILE"
            echo "Streamlit consumer started with PID $(cat $PID_FILE)."
            sleep 1
            URL=$(cat $LOG_FILE | grep 'Local URL' | sed 's/^[ \t]*//')
            echo "Consumer $URL"
        fi
        ;;
    
    stop)
        if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
            echo "Stopping Streamlit consumer app with PID $(cat $PID_FILE)..."
            kill $(cat "$PID_FILE")
            rm "$PID_FILE"
            echo "Streamlit consumer stopped."
        else
            echo "Streamlit consumer is not running."
        fi
        ;;

    restart)
        $0 stop
        sleep 1
        $0 start
        ;;

    status)
        if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
            echo "Streamlit consumer is running with PID $(cat $PID_FILE)."
            URL=$(cat $LOG_FILE | grep 'Local URL' | sed 's/^[ \t]*//')
            echo "Consumer $URL"
            echo ""
        else
            echo "Streamlit consumer is not running."
        fi
        ;;

    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

