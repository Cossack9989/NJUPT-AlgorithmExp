/*
 * 魔王语言
 * 栈----先进后出-----处理带括号的部分
 * 队列--先进先出-----将对处理后的语言
 * 2018.10.3 fang
 */
#include<stdio.h>
#include<stdlib.h>
#define STACK_INIT_SIZE 100;        //存储空间初始分配量
#define STACKINCREMENT 10;          //存储空间分配增量
#define NULL 0;

/*
    输入检验：   1.   B(ehnxgz)B                     输出： tsaedsaeezegexenehetsaedsae
                 2.   B(ab(cde)fg)B                   输出： tsaedsaeagafacadacaeacabatsaedsae
                 3.   #BooooooMAoo今天天气不错！     输出： #tsaedsaeooooooMsaeoo今天天气不错！ 
*/


typedef struct Sqstack{
    char *base;
    char *top;
    int stacksize;
}sqstack;

typedef struct QNode{
    char data;
    struct QNode *next;
}Qnode, *QueuePtr;

typedef struct LinkQueue{
    QueuePtr front;
    QueuePtr rear;
}LinkQueue;
//初始化栈
void InitStack(sqstack *s);
//入栈
void push(sqstack *s,char e);
//出栈 
char Pop(sqstack *s);
//初始化队列
void InitQueue(LinkQueue *q);
//入队
void Enqueue(LinkQueue *q,char e);
//出队
char Dequeue(LinkQueue *q);


int main() {
    sqstack *s;
    LinkQueue *q;
    int m, j;
    int i = 0;
    int count = 0; 
    char c, language[1000];
    q = (LinkQueue*)malloc(sizeof(LinkQueue));
    s = (sqstack*)malloc(sizeof(sqstack));
    InitStack(s);
    InitQueue(q);
    //① 首先，将魔王语言存放在language数组中
    printf("\t\t*************** Devil's Language ***************\n\n\n");
    printf("\t\t请输入魔王语言:\t");
    while(c != '\n') {
        scanf("%c",&c);
        if(c == '(') count++;
        language[i] = c;
        i++;
    }
    i--;

if(count == 0){
} else{
        while(count >= 1){
            int k1 = 0;
        //② 然后，将数组中 第count重括号，(用k1来表示循环到第几重)内元素入栈(括号里的元素放在栈中逆置)
        //从第二位数字开始，每位数字后面都插入括号里数据的首字母
        
        for(j=0;j<=i;j++) {
            if(language[j] == '(') {     
                k1++;
                if(k1==count){     
                    m = j; // language[m+1]作为固定的首字母值
                    push(s,language[m+1]);
                    while(language[j+2] != ')'){
                        push(s,language[j+2]);
                        push(s,language[m+1]);
                        j++;
                    }
                    break;
                }else j++;            
            }
        }
    
        //③ 将数组中元素全部入队，遇到存入栈的（）先出栈再入队
        for(j=0; j<=i; j++) {
            if(language[j] == '(' && j==m) { 
                    while(s->base != s->top) {
                        char e = Pop(s);
                        Enqueue(q,e);
                    }
                    while(language[j] != ')'){
                        j++;
                        continue;
                       }       
            }else if(count==1 && (language[j]=='(' || language[j]==')')){
                
            }else Enqueue(q,language[j]);
        }
        
        
        count--;
        i = 0;
        while(q->front != q->rear){
            language[i] = Dequeue(q);
            i++;
        }
        
    }
}

    //④ 将队中的元素全部取出，逐个翻译
    printf("\n\n\t\t翻译之后：\t");
    for(j = 0; j<=i; j++) {
        char ch = language[j];
        if(ch == 'A')                      printf("%s","sae");
        else if(ch == 'B')               printf("%s","tsaedsae");
        else                              printf("%c",ch);
    }
    return 0;  
    
}











//栈操作
void InitStack(sqstack *s) {
    s->base = (char*) malloc(100 * sizeof(char));
    s->top = s->base;
    s->stacksize = STACK_INIT_SIZE;
}
//压栈 
void push(sqstack *s,char e) {
    //如果栈满
    if(s->top - s->base >= s->stacksize) {
        s->base = (char *)realloc(s->base,(s->stacksize+10)*sizeof(char));
        s->stacksize += STACKINCREMENT;
        s->top = s->base + s->stacksize;
    }
    *(s->top) = e;
    s->top++;
}
//出栈 
char Pop(sqstack *s) {
    char e;
    if(s->top-s->base == 0)
        return -1;
    --s->top;
    e = *(s->top);
    return e;
}





//队列操作
void InitQueue(LinkQueue *q){
    q->front = q->rear = (QueuePtr)malloc(sizeof(Qnode));
    if(!q->front) exit(-1);    //内存分配失败 
    q->front->next = NULL;
}
//入队 
void Enqueue(LinkQueue *q,char e){
    QueuePtr p = (QueuePtr)malloc(sizeof(Qnode));
    if(!p) exit(-1);       //内存分配失败 
    p->data = e;
    p->next = NULL;
    q->rear->next = p;
    q->rear = p;
}
//出队 
char Dequeue(LinkQueue *q){
    char e;
    if(q->front == q->rear)    exit(0); 
    QueuePtr p = q->front->next;
    e = p->data;
    q->front->next = p->next;
    if(q->rear == p)       q->rear = q->front;
    free(p);
    return e;
}