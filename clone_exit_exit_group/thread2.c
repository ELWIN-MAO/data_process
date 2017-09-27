// gcc  -lpthread
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

void *thread_function(void *arg);
void *thread_function2(void *arg);

char message[] = "thread1";

int main() {
    int res;
    pthread_t a_thread;
    void *thread_result;
    printf("main thread\n");
    res = pthread_create(&a_thread, NULL, thread_function, (void *)message);
    if (res != 0) {
        perror("Thread creation failed");
        exit(EXIT_FAILURE);
    }
    //printf("Waiting for thread to finish...\n");
    sleep(8);
    //res = pthread_join(a_thread, &thread_result);
    //if (res != 0) {
    //    perror("Thread join failed");
    //    exit(EXIT_FAILURE);
    //}
    //printf("Thread joined, it returned %s\n", (char *)thread_result);
    //printf("Message is now %s\n", message);
    //exit(EXIT_SUCCESS);
    printf("main thread exit\n");
    //pthread_exit("abcd");
    pthread_exit("5");
    exit(7);
    return 5;
}

void *thread_function(void *arg) {
    pthread_t a_thread2;
    int res;
    res = pthread_create(&a_thread2, NULL, thread_function2, "thread2");
    printf("thread_function is running. Argument was %s\n", (char *)arg);
    sleep(30);
    printf("thread1 exit\n");
    //strcpy(message, "Bye!");
    //pthread_exit("Thank you for the CPU time");
    exit(8);
   return "abc";
}



void *thread_function2(void *arg) {
    printf("thread_function is running. Argument was %s\n", (char *)arg);
    sleep(20);
    //strcpy(message, "Bye!");
    printf("thread2 exit\n");
    pthread_exit("Thank you for the CPU time");
   exit(6);
   //return 4;
   return "def";
}
