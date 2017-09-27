// gcc  -lpthread
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

void *thread_function(void *arg);
void *thread_function2(void *arg);

char message[] = "Hello World";

int main() {
    int res;
    pthread_t a_thread;
    void *thread_result;
    res = pthread_create(&a_thread, NULL, thread_function, (void *)message);
    if (res != 0) {
        perror("Thread creation failed");
        exit(EXIT_FAILURE);
    }
    printf("Waiting for thread to finish...\n");
    sleep(20);
    res = pthread_join(a_thread, &thread_result);
    if (res != 0) {
        perror("Thread join failed");
        exit(EXIT_FAILURE);
    }
    printf("Thread joined, it returned %s\n", (char *)thread_result);
    printf("Message is now %s\n", message);
    exit(EXIT_SUCCESS);
}

void *thread_function(void *arg) {
    pthread_t a_thread2;
    int res;
    res = pthread_create(&a_thread2, NULL, thread_function2, "thread2");
    printf("thread_function is running. Argument was %s\n", (char *)arg);
    sleep(3);
    printf("thread1 exit\n");
    //strcpy(message, "Bye!");
    pthread_exit("Thank you for the CPU time");
}



void *thread_function2(void *arg) {
    printf("thread_function is running. Argument was %s\n", (char *)arg);
    sleep(8);
    //strcpy(message, "Bye!");
    printf("thread2 exit\n");
    //pthread_exit("Thank you for the CPU time");
   exit(77);
}
