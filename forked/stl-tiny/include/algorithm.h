#ifndef  _ALGORITHM_H_
#define  _ALGORITHM_H_

/*

   algorighm   



 */

#include "iterator.h"
#include "functional.h"
#include "iterator.h"

namespace  h_stl {
    /*
       定义迭代器辅助函数
       advance   迭代器移动固定距离
     */

    //重载输入迭代器
    template<typename  InputIterator, typename Distance>
        void _advance(InputIterator& iter, Distance d, input_iterator_tag) {

            assert(d >= 0);
            while(d--) { iter++;}
        }
    template<typename  InputIterator, typename  Distance>
        void _advance(InputIterator& iter, Distance d, bidirectional_iterator_tag) {

            if(d < 0) {
                while(d ++) {
                    --iter;
                }  
            }else {
                while(d --) {
                    ++iter; 
                }
            }
        }
    template<typename InputIterator, typename  Distance>
        void _advance(InputIterator& iter, Distance d, random_access_iterator_tag) {

            if(d < 0) {
                iter -= (-d);  
            }else {
                iter += d;   
            }
        }
    template<typename InputIterator, typename Distance>
        void advance(InputIterator &iter, Distance d) {

            typedef typename iterator_traits<InputIterator>::iterator_category iterator_category;
            _advance(iter, d, iterator_category());
        }




    /*
       定义迭代器辅助函数
       distance  计算迭代器距离 
     */
    template<class InputIterator>
        typename iterator_traits<InputIterator>::difference_type
        _distance(InputIterator first, InputIterator last, input_iterator_tag) {

            typename iterator_traits<InputIterator>::difference_type dist = 0;  
            while(first++ != last) {
                ++dist; 
            }
            return dist;
        }
    template<class RandomIterator>
        typename iterator_traits<RandomIterator>::difference_type
        _distance(RandomIterator first, RandomIterator last, random_access_iterator_tag) {
            auto dist = last - first;
            return dist;
        }
    template<class Iterator>
        typename  iterator_traits<Iterator>::difference_type
        distance(Iterator first, Iterator last) {
            typedef typename iterator_traits<Iterator>::iterator_category iterator_category;
            return _distance(first, last, iterator_category());
        }


}


#endif
