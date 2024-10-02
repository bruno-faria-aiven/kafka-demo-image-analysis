#!/bin/bash

case "$1" in
    start)
        ./start_producer.sh start ; ./start_consumer.sh start
        ;;
    
    stop)
        ./start_producer.sh stop ; ./start_consumer.sh stop
        ;;

    restart)
        $0 stop
        sleep 1
        $0 start
        ;;

    status)
        ./start_producer.sh status ; ./start_consumer.sh status
        ;;

    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

