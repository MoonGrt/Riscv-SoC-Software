#include <rthw.h>
#include <finsh_config.h>

#ifdef RT_USING_FINSH

#include "finsh.h"
#include "shell.h"
#include "cyber.h"

#ifdef FINSH_USING_MSH
#include "msh.h"
#endif

#define NULL ((void *)0)

#ifndef RT_USING_HEAP
/* finsh 线程控制块 */
static struct rt_thread finsh_thread;

/* finsh 线程栈 */
ALIGN(RT_ALIGN_SIZE)
static char finsh_thread_stack[FINSH_THREAD_STACK_SIZE];

/* finsh_shell 结构体 */
struct finsh_shell _shell;
#endif

/* finsh symtab */
#ifdef FINSH_USING_SYMTAB
struct finsh_syscall *_syscall_table_begin = NULL;
struct finsh_syscall *_syscall_table_end   = NULL;
#endif

struct finsh_shell *shell;

const char *finsh_get_prompt()
{
#define _MSH_PROMPT "msh >"

    static char finsh_prompt[RT_CONSOLEBUF_SIZE + 1] = {0};
    
    rt_strncpy(finsh_prompt, _MSH_PROMPT, RT_CONSOLEBUF_SIZE);

    return finsh_prompt;
}

// char uart_getc()
// {
// 	int ch = -1;

// 	// wait RI to 1
// 	if ((uart_read_reg(UART_CTRL) & (1 << 0)) != (1 << 0))
// 		return -1;
// 	// set RI to 0
// 	uart_write_reg(UART_CTRL, (uart_read_reg(UART_CTRL) & ~(1 << 0)));
// 	// read receive buf
// 	ch = uart_read_reg(UART_RX_DATA_BUF);

// 	return ch;
// }

static int finsh_getchar(void)
{
	// int ch = uart_getc();
    int ch = USART_ReceiveData(USART1);
    
    /* 如果未获取到字符，则让出处理器 */
    if (ch < 0)
    {
        rt_thread_delay(1);
    }

    return ch;
}

extern void delay(unsigned int);

/* finsh 线程入口函数 */
void finsh_thread_entry(void *parameter)
{
    int ch;

    /* normal is echo mode */
    shell->echo_mode = 1;
    
    printf("Welcome to RT-Thread's World!\r\n");

    printf(FINSH_PROMPT);

    while (1)
    {
        ch = finsh_getchar();

        if (ch < 0)
        {
            continue;
        }

        /* received null or error */
        if (ch == '\0' || ch == 0xFF)
        {
            continue;
        }
        /* handle tab key */
        else if (ch == '\t')
        {
            printf("tab key!\r\n");
            continue;
        }
        /* handle backspace or del key */
        else if (ch == 0x7f || ch == 0x08)
        {
            if (shell->line_curpos == 0) continue;

	        shell->line_position--;
	        shell->line_curpos--;

	        printf("\b \b");
	        shell->line[shell->line_position] = 0;

	        continue;
        }
        
        /* handle end of line, break */
        if (ch == '\r' || ch == '\n')
        {
            //printf("\r\nreceived your command: %s\r\n", shell->line);
            if (shell->echo_mode)
                printf("\r\n");
                
            msh_exec(shell->line, shell->line_position);
            
            printf(FINSH_PROMPT);

	        rt_memset(shell->line, 0, sizeof(shell->line));

            shell->line_curpos = shell->line_position = 0;
            continue;
        }
        
        /* it's a large line, discard it */
        if (shell->line_position >= FINSH_CMD_SIZE)
            shell->line_position = 0;

        /* normal character */
        shell->line[shell->line_curpos] = ch;
        if (shell->echo_mode)
            printf("%c", ch);
        
        ch = 0;
        shell->line_position++;
        shell->line_curpos++;
        if (shell->line_position >= FINSH_CMD_SIZE)
        {
            /* clear command line */
            shell->line_position = 0;
            shell->line_curpos = 0;
        }
    }
}
// void finsh_thread_entry(void *parameter)
// {
//     int ch;

//     /* normal is echo mode */
// #ifndef FINSH_ECHO_DISABLE_DEFAULT
//     shell->echo_mode = 1;
// #else
//     shell->echo_mode = 0;
// #endif

// #if !defined(RT_USING_POSIX_STDIO) && defined(RT_USING_DEVICE)
//     /* set console device as shell device */
//     if (shell->device == RT_NULL)
//     {
//         rt_device_t console = rt_console_get_device();
//         if (console)
//         {
//             finsh_set_device(console->parent.name);
//         }
//     }
// #endif /* !defined(RT_USING_POSIX_STDIO) && defined(RT_USING_DEVICE) */

// #ifdef FINSH_USING_AUTH
//     /* set the default password when the password isn't setting */
//     if (rt_strlen(finsh_get_password()) == 0)
//     {
//         if (finsh_set_password(FINSH_DEFAULT_PASSWORD) != RT_EOK)
//         {
//             printf("Finsh password set failed.\n");
//         }
//     }
//     /* waiting authenticate success */
//     finsh_wait_auth();
// #endif

//     printf(FINSH_PROMPT);

//     while (1)
//     {
//         ch = (int)finsh_getchar();
//         if (ch < 0)
//         {
//             continue;
//         }

//         /*
//          * handle control key
//          * up key  : 0x1b 0x5b 0x41
//          * down key: 0x1b 0x5b 0x42
//          * right key:0x1b 0x5b 0x43
//          * left key: 0x1b 0x5b 0x44
//          */
//         if (ch == 0x1b)
//         {
//             shell->stat = WAIT_SPEC_KEY;
//             continue;
//         }
//         else if (shell->stat == WAIT_SPEC_KEY)
//         {
//             if (ch == 0x5b)
//             {
//                 shell->stat = WAIT_FUNC_KEY;
//                 continue;
//             }

//             shell->stat = WAIT_NORMAL;
//         }
//         else if (shell->stat == WAIT_FUNC_KEY)
//         {
//             shell->stat = WAIT_NORMAL;

//             if (ch == 0x41) /* up key */
//             {
// #ifdef FINSH_USING_HISTORY
//                 /* prev history */
//                 if (shell->current_history > 0)
//                     shell->current_history --;
//                 else
//                 {
//                     shell->current_history = 0;
//                     continue;
//                 }

//                 /* copy the history command */
//                 rt_memcpy(shell->line, &shell->cmd_history[shell->current_history][0],
//                        FINSH_CMD_SIZE);
//                 shell->line_curpos = shell->line_position = strlen(shell->line);
//                 shell_handle_history(shell);
// #endif
//                 continue;
//             }
//             else if (ch == 0x42) /* down key */
//             {
// #ifdef FINSH_USING_HISTORY
//                 /* next history */
//                 if (shell->current_history < shell->history_count - 1)
//                     shell->current_history ++;
//                 else
//                 {
//                     /* set to the end of history */
//                     if (shell->history_count != 0)
//                         shell->current_history = shell->history_count - 1;
//                     else
//                         continue;
//                 }

//                 rt_memcpy(shell->line, &shell->cmd_history[shell->current_history][0],
//                        FINSH_CMD_SIZE);
//                 shell->line_curpos = shell->line_position = strlen(shell->line);
//                 shell_handle_history(shell);
// #endif
//                 continue;
//             }
//             else if (ch == 0x44) /* left key */
//             {
//                 if (shell->line_curpos)
//                 {
//                     printf("\b");
//                     shell->line_curpos --;
//                 }

//                 continue;
//             }
//             else if (ch == 0x43) /* right key */
//             {
//                 if (shell->line_curpos < shell->line_position)
//                 {
//                     printf("%c", shell->line[shell->line_curpos]);
//                     shell->line_curpos ++;
//                 }

//                 continue;
//             }
//         }

//         /* received null or error */
//         if (ch == '\0' || ch == 0xFF) continue;
//         /* handle tab key */
//         else if (ch == '\t')
//         {
//             int i;
//             /* move the cursor to the beginning of line */
//             for (i = 0; i < shell->line_curpos; i++)
//                 printf("\b");

//             /* auto complete */
//             shell_auto_complete(&shell->line[0]);
//             /* re-calculate position */
//             shell->line_curpos = shell->line_position = strlen(shell->line);

//             continue;
//         }
//         /* handle backspace key */
//         else if (ch == 0x7f || ch == 0x08)
//         {
//             /* note that shell->line_curpos >= 0 */
//             if (shell->line_curpos == 0)
//                 continue;

//             shell->line_position--;
//             shell->line_curpos--;

//             if (shell->line_position > shell->line_curpos)
//             {
//                 int i;

//                 rt_memmove(&shell->line[shell->line_curpos],
//                            &shell->line[shell->line_curpos + 1],
//                            shell->line_position - shell->line_curpos);
//                 shell->line[shell->line_position] = 0;

//                 printf("\b%s  \b", &shell->line[shell->line_curpos]);

//                 /* move the cursor to the origin position */
//                 for (i = shell->line_curpos; i <= shell->line_position; i++)
//                     printf("\b");
//             }
//             else
//             {
//                 printf("\b \b");
//                 shell->line[shell->line_position] = 0;
//             }

//             continue;
//         }

//         /* handle end of line, break */
//         if (ch == '\r' || ch == '\n')
//         {
// #ifdef FINSH_USING_HISTORY
//             shell_push_history(shell);
// #endif
//             if (shell->echo_mode)
//                 printf("\n");
//             msh_exec(shell->line, shell->line_position);

//             printf(FINSH_PROMPT);
//             rt_memset(shell->line, 0, sizeof(shell->line));
//             shell->line_curpos = shell->line_position = 0;
//             continue;
//         }

//         /* it's a large line, discard it */
//         if (shell->line_position >= FINSH_CMD_SIZE)
//             shell->line_position = 0;

//         /* normal character */
//         if (shell->line_curpos < shell->line_position)
//         {
//             int i;

//             rt_memmove(&shell->line[shell->line_curpos + 1],
//                        &shell->line[shell->line_curpos],
//                        shell->line_position - shell->line_curpos);
//             shell->line[shell->line_curpos] = ch;
//             if (shell->echo_mode)
//                 printf("%s", &shell->line[shell->line_curpos]);

//             /* move the cursor to new position */
//             for (i = shell->line_curpos; i < shell->line_position; i++)
//                 printf("\b");
//         }
//         else
//         {
//             shell->line[shell->line_position] = ch;
//             if (shell->echo_mode)
//                 printf("%c", ch);
//         }

//         ch = 0;
//         shell->line_position ++;
//         shell->line_curpos++;
//         if (shell->line_position >= FINSH_CMD_SIZE)
//         {
//             /* clear command line */
//             shell->line_position = 0;
//             shell->line_curpos = 0;
//         }
//     } /* end of device read */
// }












void finsh_system_function_init(const void *begin, const void *end)
{
    _syscall_table_begin = (struct finsh_syscall *) begin;
    _syscall_table_end = (struct finsh_syscall *) end;
}

/* finsh 线程初始化函数 */
int finsh_system_init(void)
{
    rt_err_t result = RT_EOK;
    rt_thread_t tid;

    /* GNU GCC Compiler and TI CCS */
    extern const int __fsymtab_start;
    extern const int __fsymtab_end;
    finsh_system_function_init(&__fsymtab_start, &__fsymtab_end);

    shell = &_shell;
    tid = &finsh_thread;
    result = rt_thread_init(&finsh_thread,
                            FINSH_THREAD_NAME,
                            finsh_thread_entry,
                            RT_NULL,
                            &finsh_thread_stack[0],
                            sizeof(finsh_thread_stack),
                            FINSH_THREAD_PRIORITY,
                            10);
    
    if (tid != NULL && result == RT_EOK)
        rt_thread_startup(tid);
    return 0;
}

#endif /* RT_USING_FINSH */
