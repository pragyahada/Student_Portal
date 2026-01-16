/*
SQLyog Community
MySQL - 10.4.32-MariaDB : Database - student_portal
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`student_portal` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `student_portal`;

/*Table structure for table `accountantdata` */

DROP TABLE IF EXISTS `accountantdata`;

CREATE TABLE `accountantdata` (
  `name` varchar(100) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `address` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `accountantdata` */

insert  into `accountantdata`(`name`,`contact`,`email`,`address`) values 
('Karthik Reddy','9012345678','karthik.reddy@gmail.com','H.No. 44-12, Silicon Residency, Madhapur, Hyderabad, Telangana - 500081'),
('Ram Kumar Verma','6985415852','ram.kumar@gmail.com','Mahaveer Nagar I, Parijat Colony, Kota, Rajasthan,324005'),
('Rohan Singh','9901234567','rohan.singh@gmail.com','Block A-119, Rajouri Garden Extension, New Delhi - 110027');

/*Table structure for table `admindata` */

DROP TABLE IF EXISTS `admindata`;

CREATE TABLE `admindata` (
  `name` varchar(100) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `address` varchar(100) NOT NULL,
  PRIMARY KEY (`address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `admindata` */

insert  into `admindata`(`name`,`contact`,`email`,`address`) values 
('Vigneshwaran Murugan','9094421567','vigneshwaran.murugan@gmail.com','11, Anna Salai, Chennai, Tamil Nadu, India'),
('Tanmayi Bhosale','9810234476','tanmayi.bhosale@gmail.com','42, Shaniwar Peth, Pune, Maharashtra, India'),
('Rahul Sharma','9876543210','rahul.sharma@gmail.com','Flat No. 204, Green Valley Apartments, Andheri East, Mumbai, Maharashtra - 400059'),
('Priya Verma','  9123456789','priya.verma@gmail.com','House No. 78, Sector 15, Near Huda Market, Gurugram, Haryana - 122001');

/*Table structure for table `coursedata` */

DROP TABLE IF EXISTS `coursedata`;

CREATE TABLE `coursedata` (
  `course_id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) DEFAULT NULL,
  `student_name` varchar(100) DEFAULT NULL,
  `course_name` varchar(100) DEFAULT NULL,
  `course_fees` int(100) DEFAULT NULL,
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `coursedata` */

insert  into `coursedata`(`course_id`,`student_id`,`student_name`,`course_name`,`course_fees`) values 
(3,1,'Aarav Gupta','Database Management (SQL & NoSQL)',25000),
(7,1,'Aarav Gupta','UI/UX Design',30000),
(8,2,'Isha Sharma','Web Development Fundamentals',25000),
(9,0,'','Database Management (SQL & NoSQL)',15000),
(10,0,'','Artificial Intelligence (AI)',45000),
(11,2,'Isha Sharma','Artificial Intelligence (AI)',15000),
(12,2,'Isha Sharma','Cloud Computing (AWS & Azure)',9000);

/*Table structure for table `logindata` */

DROP TABLE IF EXISTS `logindata`;

CREATE TABLE `logindata` (
  `email` varchar(100) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  `usertype` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `logindata` */

insert  into `logindata`(`email`,`password`,`usertype`) values 
('aarav.gupta@gmail.com','student123','student'),
('ananya.reddy@gmail.com','student123','student'),
('arnav.mehta@gmail.com','student123','student'),
('isha.sharma@gmail.com','student123','student'),
('kabir.singh@gmail.com','student123','student'),
('karthik.reddy@gmail.com','account123','accountant'),
('priya.verma@gmail.com','admin123','admin'),
('rahul.sharma@gmail.com','admin123','admin'),
('ram.kumar@gmail.com','account123','accountant'),
('ravi.gupta@gmail.com','admin123','admin'),
('riya.patel@gmail.com','student123','student'),
('rohan.singh@gmail.com','account123','accountant'),
('tanmayi.bhosale@gmail.com','admin123','admin'),
('vigneshwaran.murugan@gmail.com','admin123','admin'),
('vivaan.kumar@gmail.com','student123','student');

/*Table structure for table `photodata` */

DROP TABLE IF EXISTS `photodata`;

CREATE TABLE `photodata` (
  `email` varchar(100) NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `photodata` */

insert  into `photodata`(`email`,`photo`) values 
('priya.verma@gmail.com','1766468602.jpg');

/*Table structure for table `studentdata` */

DROP TABLE IF EXISTS `studentdata`;

CREATE TABLE `studentdata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `gender` varchar(100) DEFAULT NULL,
  `joining_date` date DEFAULT NULL,
  `father_name` varchar(100) DEFAULT NULL,
  `mother_name` varchar(100) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `address` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`,`email`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `studentdata` */

insert  into `studentdata`(`id`,`name`,`gender`,`joining_date`,`father_name`,`mother_name`,`contact`,`email`,`address`) values 
(1,'Aarav Gupta','Male','2025-01-11','Ram Gupta','Neha Gupta','9876501234','aarav.gupta@gmail.com','Flat 12B, Sunrise Apartments, Shastri Nagar, Kanpur, Uttar Pradesh - 208005'),
(2,'Isha Sharma','Female','2025-01-11','Amit Sharma','Pooja Sharma','9867543201','isha.sharma@gmail.com','House No. 45, Royal Residency, Civil Lines, Jaipur, Rajasthan - 302006'),
(3,'Vivaan Kumar','Male','2025-01-12','Sanjay Kumar','Ritu Kumar','9856021345','vivaan.kumar@gmail.com','B-27, Steel Township Quarters, Sector 4, Bokaro Steel City, Jharkhand - 827004'),
(4,'Ananya Reddy','Female','2025-01-13','Srinivas Reddy','Lakshmi Reddy','9912347865','ananya.reddy@gmail.com','Plot No. 78, Lake View Colony, Miyapur, Hyderabad, Telangana - 500049'),
(5,'Kabir Singh','Male','2025-01-14','Rajesh Singh','Swati Singh','9988776655','kabir.singh@gmail.com','Flat 303, Dwarka Apartments, Sector 18, Noida, Uttar Pradesh - 201301'),
(6,'Riya Patel','Female','2025-01-15','Dharmesh Patel','Kajal Patel','9877012456','riya.patel@gmail.com','B-09, Lotus Valley Society, Akota, Vadodara, Gujarat - 390020'),
(7,'Arnav Mehta','Male','2025-01-16','Vikram Mehta','Manisha Mehta','9823100567','arnav.mehta@gmail.com','Row House 11, Green Park Villas, Kothrud, Pune, Maharashtra - 411038'),
(11,'qqq','Male','2025-12-23','qqq','qqq','8989898989','qqq@gmail.com','qqq');

/*Table structure for table `transactiondata` */

DROP TABLE IF EXISTS `transactiondata`;

CREATE TABLE `transactiondata` (
  `transaction_id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) DEFAULT NULL,
  `student_name` varchar(100) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  `course_name` varchar(100) DEFAULT NULL,
  `deposit_amount` int(11) DEFAULT NULL,
  `deposit_date` date DEFAULT NULL,
  `payment_method` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`transaction_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `transactiondata` */

insert  into `transactiondata`(`transaction_id`,`student_id`,`student_name`,`course_id`,`course_name`,`deposit_amount`,`deposit_date`,`payment_method`) values 
(1,1,'Aarav Gupta',1,'DSA',10000,'2024-02-06','Cash'),
(2,1,'Aarav Gupta',1,'DSA',500,'2025-11-21','Credit'),
(3,1,'Aarav Gupta',3,'Database Management (SQL & NoSQL)',1500,'2025-11-21','Cash'),
(4,1,'Aarav Gupta',5,'Web Development Fundamentals',3500,'2025-11-21','UPI'),
(5,1,'Aarav Gupta',6,'Artificial Intelligence (AI)',2500,'2025-11-22','Cash'),
(6,1,'Aarav Gupta',3,'Database Management (SQL & NoSQL)',15000,'2025-11-11','UPI'),
(7,1,'Aarav Gupta',7,'UI/UX Design',3600,'2025-11-24','Credit'),
(8,1,'Aarav Gupta',7,'UI/UX Design',100,'2025-11-25','Cash'),
(9,2,'Isha Sharma',8,'Web Development Fundamentals',12000,'2025-11-29','UPI'),
(10,2,'Isha Sharma',11,'Artificial Intelligence (AI)',6900,'2025-11-29','Credit'),
(11,2,'Isha Sharma',12,'Cloud Computing (AWS & Azure)',5000,'2025-11-29','Cash');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
