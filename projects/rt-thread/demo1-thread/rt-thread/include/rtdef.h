#ifndef __RT_DEF_H__
#define __RT_DEF_H__

/* RT-Thread basic data type definitions */
typedef signed   char                   rt_int8_t;      /**<  8bit integer type                  */
typedef signed   short                  rt_int16_t;     /**< 16bit integer type                  */
typedef signed   int                    rt_int32_t;     /**< 32bit integer type                  */
typedef unsigned char                   rt_uint8_t;     /**<  8bit unsigned integer type         */
typedef unsigned short                  rt_uint16_t;    /**< 16bit unsigned integer type         */
typedef unsigned int                    rt_uint32_t;    /**< 32bit unsigned integer type         */

typedef int                             rt_bool_t;      /**< boolean type                        */
typedef long                            rt_base_t;      /**< Nbit CPU related date type          */
typedef unsigned long                   rt_ubase_t;     /**< Nbit unsigned CPU related data type */

typedef rt_base_t                       rt_err_t;       /**< Type for error number               */
typedef rt_uint32_t                     rt_time_t;      /**< Type for time stamp                 */
typedef rt_uint32_t                     rt_tick_t;      /**< Type for tick count                 */
typedef rt_base_t                       rt_flag_t;      /**< Type for flags                      */
typedef rt_ubase_t                      rt_size_t;      /**< Type for size number                */
typedef rt_ubase_t                      rt_dev_t;       /**< Type for device                     */
typedef rt_base_t                       rt_off_t;       /**< Type for offset                     */

/* boolean type definitions */
#define RT_TRUE                         1               /**< boolean true            */
#define RT_FALSE                        0               /**< Type for false          */

/* RT-Thread error code definitions */
#define RT_EOK                          0               /**< There is no error       */
#define RT_ERROR                        1               /**< A generic error happens */

/* Compiler Related Definitions */
#if defined (__GNUC__)                                  /* GNU GCC Compiler */
    #ifdef RT_USING_NEWLIB
        #include <stdarg.h>
    #else 
    #endif

    #define rt_inline                   static __inline
    #define ALIGN(n)                    __attribute__((aligned(n)))
#else
    #error not supported tool chain
#endif

/**
 * @ingroup BasicDef
 *
 * @def RT_ALIGN(size, align)
 * Return the most contiguous size aligned at specified width. RT_ALIGN(13, 4)
 * would return 16.
 */
#define RT_ALIGN(size, align)          (((size) + (align) -1) & ~((align) - 1))           

/**
 * @ingroup BasicDef
 *
 * @def RT_ALIGN_DOWN(size, align)
 * Return the down number of aligned at specified width. RT_ALIGN_DOWN(13, 4)
 * would return 12.
 */
#define RT_ALIGN_DOWN(size, align)     ((size) & ~((align) - 1))

#define RT_NULL                        (0)

/**
 * Double List structure
 */
struct rt_list_node
{
    struct rt_list_node *next;                          /**< point to next node. */
    struct rt_list_node *prev;                          /**< point to prev node. */
};
typedef struct rt_list_node rt_list_t;                  /**< Type for lists. */

/**
 * Single List structure 
 */
struct rt_slist_node
{
    struct rt_slist_node *next;                         /**< point to prev node. */
};
typedef struct rt_slist_node rt_slist_t;                /**< Type for single lists. */


/**
 * Thread structure 
 */
struct rt_thread
{
    /* rt object */
    rt_list_t   tlist;                          /**< 线程链表节点 */

    /* stack point and entry */
    void        *sp;                            /**< 线程当前栈顶指针 */
    void        *entry;                         /**< 线程函数入口 */
    void        *parameter;                     /**< 线程函数的传入参数 */
    void        *stack_addr;                    /**< 线程栈起始地址 */
    rt_uint32_t  stack_size;                    /**< 线程栈大小，单位为字节 */
};

#endif