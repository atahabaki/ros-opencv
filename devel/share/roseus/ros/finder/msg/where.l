;; Auto-generated. Do not edit!


(when (boundp 'finder::where)
  (if (not (find-package "FINDER"))
    (make-package "FINDER"))
  (shadow 'where (find-package "FINDER")))
(unless (find-package "FINDER::WHERE")
  (make-package "FINDER::WHERE"))

(in-package "ROS")
;;//! \htmlinclude where.msg.html


(defclass finder::where
  :super ros::object
  :slots (_cx _cy _distance _angle ))

(defmethod finder::where
  (:init
   (&key
    ((:cx __cx) 0)
    ((:cy __cy) 0)
    ((:distance __distance) 0.0)
    ((:angle __angle) 0.0)
    )
   (send-super :init)
   (setq _cx (round __cx))
   (setq _cy (round __cy))
   (setq _distance (float __distance))
   (setq _angle (float __angle))
   self)
  (:cx
   (&optional __cx)
   (if __cx (setq _cx __cx)) _cx)
  (:cy
   (&optional __cy)
   (if __cy (setq _cy __cy)) _cy)
  (:distance
   (&optional __distance)
   (if __distance (setq _distance __distance)) _distance)
  (:angle
   (&optional __angle)
   (if __angle (setq _angle __angle)) _angle)
  (:serialization-length
   ()
   (+
    ;; uint64 _cx
    8
    ;; uint64 _cy
    8
    ;; float32 _distance
    4
    ;; float32 _angle
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint64 _cx
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _cx (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _cx) (= (length (_cx . bv)) 2)) ;; bignum
              (write-long (ash (elt (_cx . bv) 0) 0) s)
              (write-long (ash (elt (_cx . bv) 1) -1) s))
             ((and (class _cx) (= (length (_cx . bv)) 1)) ;; big1
              (write-long (elt (_cx . bv) 0) s)
              (write-long (if (>= _cx 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _cx s)(write-long (if (>= _cx 0) 0 #xffffffff) s)))
     ;; uint64 _cy
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _cy (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _cy) (= (length (_cy . bv)) 2)) ;; bignum
              (write-long (ash (elt (_cy . bv) 0) 0) s)
              (write-long (ash (elt (_cy . bv) 1) -1) s))
             ((and (class _cy) (= (length (_cy . bv)) 1)) ;; big1
              (write-long (elt (_cy . bv) 0) s)
              (write-long (if (>= _cy 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _cy s)(write-long (if (>= _cy 0) 0 #xffffffff) s)))
     ;; float32 _distance
       (sys::poke _distance (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _angle
       (sys::poke _angle (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint64 _cx
     
#+(or :alpha :irix6 :x86_64)
      (setf _cx (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _cx (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; uint64 _cy
     
#+(or :alpha :irix6 :x86_64)
      (setf _cy (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _cy (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; float32 _distance
     (setq _distance (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _angle
     (setq _angle (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get finder::where :md5sum-) "1fa8de026066c3b6956b884103782c6e")
(setf (get finder::where :datatype-) "finder/where")
(setf (get finder::where :definition-)
      "uint64 cx
uint64 cy
float32 distance
float32 angle

")



(provide :finder/where "1fa8de026066c3b6956b884103782c6e")


