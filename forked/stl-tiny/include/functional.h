
/*
    定义函数对象 
*/

//一元函数对象的基类
template<class T>
struct unary_function {

    typedef T argument_type;  //参数类型
    typedef T result_type;  //返回值类型
};


//二元函数基类
template<class T>
struct binary_function {

    typedef T first_argument_type;  //参数类型
    typedef T second_argument_type;  //参数类型
    typedef T result_type;   //返回值类型

};


//less  返回较小值
template<class T>
struct less{

    typedef T first_argument_type;
    typedef T second_argument_type;
    typedef bool result_type;

    result_type operator()(const first_argument_type& x, const second_argument_type& y){
        return x < y; 
    }

};

//equal_to  判断是否相等
template<class T>
struct equal_to{

    typedef T first_argument_type;
    typedef T second_argument_type;
    typedef bool result_type;

    result_type operator()(const first_argument_type& x, const second_argument_type& y) {
        return x == y; 
    }

};

//identity 验证同一性
template<class T>
struct identity : public unary_function<T> {
    const T& operator()(const T& x) const{
       return x; 
    }   
};


//select1st  返回键值  map
template<class T>
struct select1st : public unary_function<T> {
    const typename T::first_type& operator()(const T& x) const{
        return x.first; 
    }
};


