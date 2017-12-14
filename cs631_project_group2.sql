-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 14, 2017 at 05:29 AM
-- Server version: 10.1.28-MariaDB
-- PHP Version: 7.1.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cs631_project_group2`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `ID` varchar(20) NOT NULL,
  `PASSWARD` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`ID`, `PASSWARD`) VALUES
('Leon', '456'),
('Mike', '123'),
('Zhenbo', '789');

-- --------------------------------------------------------

--
-- Table structure for table `author`
--

CREATE TABLE `author` (
  `AUTHORID` varchar(20) NOT NULL,
  `ANAME` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `author`
--

INSERT INTO `author` (`AUTHORID`, `ANAME`) VALUES
('001', 'Neil Gaiman'),
('002', 'Anthony Burgess'),
('003', 'Aldous Huxley');

-- --------------------------------------------------------

--
-- Table structure for table `book`
--

CREATE TABLE `book` (
  `DOCID` varchar(20) NOT NULL,
  `ISBN` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `book`
--

INSERT INTO `book` (`DOCID`, `ISBN`) VALUES
('B001', '9783641038649'),
('B002', '9788445070154'),
('B003', '9780965185196');

-- --------------------------------------------------------

--
-- Table structure for table `borrows`
--

CREATE TABLE `borrows` (
  `BORNUMBER` int(20) NOT NULL,
  `READERID` int(20) NOT NULL,
  `DOCID` varchar(20) NOT NULL,
  `COPYNO` int(20) NOT NULL,
  `LIBID` varchar(20) NOT NULL,
  `BDATE` varchar(20) NOT NULL,
  `RDATE` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `borrows`
--

INSERT INTO `borrows` (`BORNUMBER`, `READERID`, `DOCID`, `COPYNO`, `LIBID`, `BDATE`, `RDATE`) VALUES
(1, 1, 'B002', 3, 'L002', '2016-09-25', '2016-09-29'),
(2, 4, 'P002', 2, 'L003', '2017-11-1', NULL),
(3, 3, 'J001', 3, 'L003', '2017-02-02', '2017-02-27'),
(4, 1, 'B003', 5, 'L001', '2017-08-27', NULL),
(5, 2, 'B001', 1, 'L001', '2017-06-11', '2017-06-17'),
(6, 3, 'J002', 3, 'L002', '2017-07-25', NULL),
(7, 1, 'J003', 2, 'L003', '2017-12-10', NULL),
(8, 2, 'B001', 2, 'L002', '2017-12-05', NULL),
(9, 2, 'B003', 4, 'L001', '2017-12-01', NULL),
(10, 2, 'P003', 4, 'L001', '2017-12-12', NULL),
(11, 2, 'J002', 4, 'L002', '2017-12-08', NULL),
(12, 3, 'P001', 1, 'L003', '2017-12-11', NULL),
(13, 3, 'P002', 3, 'L003', '2017-11-28', NULL),
(14, 3, 'B003', 2, 'L003', '2017-11-20', NULL),
(15, 4, 'B001', 3, 'L001', '2017-12-03', NULL),
(16, 4, 'B002', 3, 'L003', '2017-12-02', NULL),
(17, 4, 'B003', 1, 'L001', '2017-12-03', NULL),
(18, 5, 'J001', 3, 'L002', '2017-12-03', NULL),
(19, 5, 'B002', 1, 'L002', '2017-12-09', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `branch`
--

CREATE TABLE `branch` (
  `LIBID` varchar(20) NOT NULL,
  `LNAME` varchar(20) NOT NULL,
  `LLOCATION` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `branch`
--

INSERT INTO `branch` (`LIBID`, `LNAME`, `LLOCATION`) VALUES
('L001', 'FIRST', 'Denver'),
('L002', 'SECOND', 'New York'),
('L003', 'THRID', 'Seattle');

-- --------------------------------------------------------

--
-- Table structure for table `chief_editor`
--

CREATE TABLE `chief_editor` (
  `EDITOR_ID` varchar(20) NOT NULL,
  `ENAME` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `chief_editor`
--

INSERT INTO `chief_editor` (`EDITOR_ID`, `ENAME`) VALUES
('004', 'P. Avgeriou'),
('005', 'Scott Acton'),
('006', 'B. Ottersten');

-- --------------------------------------------------------

--
-- Table structure for table `copy`
--

CREATE TABLE `copy` (
  `DOCID` varchar(20) NOT NULL,
  `COPYNO` int(20) NOT NULL,
  `LIBID` varchar(20) NOT NULL,
  `POSITION` varchar(20) NOT NULL,
  `STATUS` varchar(20) NOT NULL DEFAULT 'Available',
  `FREQUENCY` int(20) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `copy`
--

INSERT INTO `copy` (`DOCID`, `COPYNO`, `LIBID`, `POSITION`, `STATUS`, `FREQUENCY`) VALUES
('B001', 1, 'L001', 'L01A01', 'Available', 1),
('B001', 1, 'L002', 'L02A01', 'Available', 0),
('B001', 2, 'L001', 'L01A02', 'Reserved', 0),
('B001', 2, 'L002', 'L02A02', 'Borrowed', 1),
('B001', 3, 'L001', 'L01A03', 'Borrowed', 1),
('B001', 3, 'L002', '', 'Available', 0),
('B001', 4, 'L001', 'L01A04', 'Available', 0),
('B001', 4, 'L002', '', 'Available', 0),
('B002', 1, 'L002', 'L02A03', 'Borrowed', 1),
('B002', 1, 'L003', '', 'Available', 0),
('B002', 2, 'L002', 'L02A04', 'Available', 0),
('B002', 2, 'L003', '', 'Available', 0),
('B002', 3, 'L002', 'L02A05', 'Available', 0),
('B002', 3, 'L003', '', 'Borrowed', 1),
('B002', 4, 'L002', 'L02A06', 'Available', 0),
('B002', 4, 'L003', '', 'Available', 0),
('B002', 5, 'L003', '', 'Available', 0),
('B002', 6, 'L003', '', 'Available', 0),
('B003', 1, 'L001', '', 'Borrowed', 1),
('B003', 1, 'L003', '', 'Available', 0),
('B003', 2, 'L001', '', 'Available', 0),
('B003', 2, 'L003', '', 'Borrowed', 1),
('B003', 3, 'L001', '', 'Available', 0),
('B003', 3, 'L003', '', 'Available', 0),
('B003', 4, 'L001', '', 'Borrowed', 1),
('B003', 5, 'L001', '', 'Borrowed', 1),
('J001', 1, 'L002', '', 'Available', 0),
('J001', 1, 'L003', 'L03B01', 'Reserved', 0),
('J001', 2, 'L002', '', 'Available', 0),
('J001', 2, 'L003', 'L03B02', 'Available', 0),
('J001', 3, 'L002', '', 'Borrowed', 1),
('J001', 3, 'L003', 'L03B03', 'Available', 1),
('J001', 4, 'L002', '', 'Available', 0),
('J001', 5, 'L002', '', 'Available', 0),
('J001', 6, 'L002', '', 'Available', 0),
('J002', 1, 'L002', 'L02B01', 'Available', 0),
('J002', 1, 'L003', '', 'Available', 0),
('J002', 2, 'L002', 'L02B02', 'Available', 0),
('J002', 2, 'L003', '', 'Available', 0),
('J002', 3, 'L002', 'L02B03', 'Borrowed', 1),
('J002', 4, 'L002', '', 'Borrowed', 1),
('J003', 1, 'L003', '', 'Available', 0),
('J003', 2, 'L003', '', 'Borrowed', 1),
('J003', 3, 'L003', '', 'Available', 0),
('J003', 4, 'L003', '', 'Available', 0),
('J003', 5, 'L003', '', 'Available', 0),
('P001', 1, 'L001', '', 'Available', 0),
('P001', 1, 'L002', '', 'Available', 0),
('P001', 1, 'L003', '', 'Borrowed', 1),
('P001', 2, 'L001', '', 'Available', 0),
('P001', 2, 'L002', '', 'Available', 0),
('P001', 2, 'L003', '', 'Available', 0),
('P001', 3, 'L001', '', 'Available', 0),
('P001', 3, 'L003', 'L03C03', 'Reserved', 0),
('P001', 4, 'L001', '', 'Available', 0),
('P002', 1, 'L002', '', 'Available', 0),
('P002', 1, 'L003', 'L03C01', 'Reserved', 0),
('P002', 2, 'L002', '', 'Available', 0),
('P002', 2, 'L003', 'L03C02', 'Borrowed', 1),
('P002', 3, 'L002', '', 'Available', 0),
('P002', 3, 'L003', 'L03C04', 'Borrowed', 1),
('P002', 5, 'L002', '', 'Available', 0),
('P003', 1, 'L001', '', 'Available', 0),
('P003', 1, 'L002', '', 'Available', 0),
('P003', 1, 'L003', '', 'Available', 0),
('P003', 2, 'L001', '', 'Available', 0),
('P003', 2, 'L002', '', 'Available', 0),
('P003', 2, 'L003', '', 'Available', 0),
('P003', 3, 'L001', '', 'Available', 0),
('P003', 3, 'L002', '', 'Available', 0),
('P003', 3, 'L003', '', 'Available', 0),
('P003', 4, 'L001', '', 'Borrowed', 1),
('P003', 4, 'L002', '', 'Available', 0),
('P003', 5, 'L002', '', 'Available', 0);

-- --------------------------------------------------------

--
-- Table structure for table `document`
--

CREATE TABLE `document` (
  `DOCID` varchar(20) NOT NULL,
  `TITLE` varchar(40) NOT NULL,
  `PDATE` varchar(20) NOT NULL,
  `PUBLISHERID` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `document`
--

INSERT INTO `document` (`DOCID`, `TITLE`, `PDATE`, `PUBLISHERID`) VALUES
('B001', 'Neverwhere', '2003-09-02', 'PB0000001'),
('B002', 'A Clockwork Orange', '1995-04-17', 'PB0000002'),
('B003', 'Brave New World', '1998-09-01', 'PB0000003'),
('J001', 'Journal of Systems and Software', '2011-06-07', 'PJ0000001'),
('J002', 'IEEE Trans. Image Process', '2016-02-13', 'PJ0000002'),
('J003', 'Signal Processing', '2017-07-14', 'PJ0000003'),
('P001', 'European Conference on Social Media', '2014-04-23', 'PP0000001'),
('P002', '5th Flow Control Conference 2010', '2010-11-08', 'PP0000002'),
('P003', 'The Leading Edge of Pervious Concrete', '2012-05-19', 'PP0000003');

-- --------------------------------------------------------

--
-- Table structure for table `fine`
--

CREATE TABLE `fine` (
  `READERID` int(20) NOT NULL,
  `FINE` decimal(20,2) NOT NULL,
  `OVERDUE` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fine`
--

INSERT INTO `fine` (`READERID`, `FINE`, `OVERDUE`) VALUES
(1, '17.60', 1),
(2, '0.00', 0),
(3, '24.80', 2),
(4, '4.40', 1),
(5, '0.00', 0);

-- --------------------------------------------------------

--
-- Table structure for table `inv_editor`
--

CREATE TABLE `inv_editor` (
  `DOCID` varchar(20) NOT NULL,
  `ISSUE_NO` int(20) NOT NULL,
  `IENAME` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `inv_editor`
--

INSERT INTO `inv_editor` (`DOCID`, `ISSUE_NO`, `IENAME`) VALUES
('J001', 1, 'W.K. Chan'),
('J002', 2, 'D-H. Bae'),
('J003', 3, 'C. Bird');

-- --------------------------------------------------------

--
-- Table structure for table `journal_issue`
--

CREATE TABLE `journal_issue` (
  `DOCID` varchar(20) NOT NULL,
  `ISSUE_NO` int(20) NOT NULL,
  `SCOPE` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `journal_issue`
--

INSERT INTO `journal_issue` (`DOCID`, `ISSUE_NO`, `SCOPE`) VALUES
('J001', 1, 'Programming methodology, software engineering'),
('J002', 2, 'Formation, processing, analysis, and display of images,video'),
('J003', 3, 'Deals with operations on analysis of signals');

-- --------------------------------------------------------

--
-- Table structure for table `journal_volume`
--

CREATE TABLE `journal_volume` (
  `DOCID` varchar(20) NOT NULL,
  `JVOLUME` int(20) NOT NULL,
  `EDITOR_ID` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `journal_volume`
--

INSERT INTO `journal_volume` (`DOCID`, `JVOLUME`, `EDITOR_ID`) VALUES
('J001', 84, '004'),
('J002', 92, '005'),
('J003', 136, '006');

-- --------------------------------------------------------

--
-- Table structure for table `proceedings`
--

CREATE TABLE `proceedings` (
  `DOCID` varchar(20) NOT NULL,
  `CDATE` varchar(20) NOT NULL,
  `CLOCATION` varchar(40) NOT NULL,
  `CEDITOR` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `proceedings`
--

INSERT INTO `proceedings` (`DOCID`, `CDATE`, `CLOCATION`, `CEDITOR`) VALUES
('P001', '2014-07-10', 'Brighton, United Kingdom', 'Rospigliosi, A.'),
('P002', '2010-06-28', 'Chicago, Illinois', 'D. Shepherd'),
('P003', '2009-11-08', 'New Orleans, Louisiana', 'Weiss Jr, C');

-- --------------------------------------------------------

--
-- Table structure for table `publisher`
--

CREATE TABLE `publisher` (
  `PUBLISHERID` varchar(20) NOT NULL,
  `PUBNAME` varchar(40) NOT NULL,
  `ADDRESS` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `publisher`
--

INSERT INTO `publisher` (`PUBLISHERID`, `PUBNAME`, `ADDRESS`) VALUES
('PB0000001', 'William Morrow', '10 East 53rd Street , New York'),
('PB0000002', 'W. W. Norton', '500 5th Ave # 6, New York'),
('PB0000003', 'Harper Perennial', ' 195 Broadway, New York'),
('PJ0000001', 'Elsevier', '50 Hampshire Street, MA'),
('PJ0000002', 'IEEE Trans. Image Process.', '3 Park Ave, New York, NY 10016'),
('PJ0000003', 'Elsevier', '50 Hampshire Street, MA'),
('PP0000001', 'Academic Conferences Ltd', '33 Wood Lane,Sonning Common,RG4 9SJ,UK'),
('PP0000002', 'AIAA', '12700 Sunrise Valley Dr #200, Reston, VA'),
('PP0000003', 'American Concrete Institute', '38800 Country Club Dr,Farmington H,MI');

-- --------------------------------------------------------

--
-- Table structure for table `reader`
--

CREATE TABLE `reader` (
  `READERID` int(20) NOT NULL,
  `RTYPE` varchar(20) NOT NULL,
  `RNAME` varchar(20) NOT NULL,
  `ADDRESS` varchar(30) NOT NULL,
  `FREQUENCY` int(20) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `reader`
--

INSERT INTO `reader` (`READERID`, `RTYPE`, `RNAME`, `ADDRESS`, `FREQUENCY`) VALUES
(1, 'student', 'Anne', '421 E DRACHMAN ,TUCSON,AZ', 0),
(2, 'senior citizen', 'Peter', '799 E DRAGRAM,TUCSON,AZ', 0),
(3, 'staff', 'Mike', '300 BOYLSTON AVE E,SEATTLE,WA', 0),
(4, 'student', 'Gary', '100 MAIN ST,SEATTLE,WA', 0),
(5, 'staff', 'Amy', '200 BROAD ST, NEW YORK, NY', 0);

--
-- Triggers `reader`
--
DELIMITER $$
CREATE TRIGGER `ADDREADER` AFTER INSERT ON `reader` FOR EACH ROW INSERT INTO `FINE` (`READERID`) VALUES (NEW.READERID)
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `DELETEREADERID` AFTER DELETE ON `reader` FOR EACH ROW DELETE FROM `FINE` WHERE READERID=OLD.READERID
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `reserves`
--

CREATE TABLE `reserves` (
  `RESNUMBER` int(20) NOT NULL,
  `READERID` int(20) NOT NULL,
  `DOCID` varchar(20) NOT NULL,
  `COPYNO` int(20) NOT NULL,
  `LIBID` varchar(20) NOT NULL,
  `DTIME` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `reserves`
--

INSERT INTO `reserves` (`RESNUMBER`, `READERID`, `DOCID`, `COPYNO`, `LIBID`, `DTIME`) VALUES
(1, 2, 'B001', 2, 'L001', '2017-12-11 16:04:01'),
(2, 2, 'P001', 3, 'L003', '2017-12-14 16:04:01'),
(3, 2, 'J001', 1, 'L003', '2017-12-14 20:04:01'),
(5, 2, 'P002', 1, 'L003', '2017-12-28 16:04:01');

-- --------------------------------------------------------

--
-- Table structure for table `writes`
--

CREATE TABLE `writes` (
  `AUTHORID` varchar(20) NOT NULL,
  `DOCID` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `writes`
--

INSERT INTO `writes` (`AUTHORID`, `DOCID`) VALUES
('001', 'B001'),
('002', 'B002'),
('003', 'B003');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `author`
--
ALTER TABLE `author`
  ADD PRIMARY KEY (`AUTHORID`);

--
-- Indexes for table `book`
--
ALTER TABLE `book`
  ADD PRIMARY KEY (`DOCID`);

--
-- Indexes for table `borrows`
--
ALTER TABLE `borrows`
  ADD PRIMARY KEY (`BORNUMBER`),
  ADD KEY `DOCID` (`DOCID`,`COPYNO`,`LIBID`),
  ADD KEY `READERID` (`READERID`);

--
-- Indexes for table `branch`
--
ALTER TABLE `branch`
  ADD PRIMARY KEY (`LIBID`);

--
-- Indexes for table `chief_editor`
--
ALTER TABLE `chief_editor`
  ADD PRIMARY KEY (`EDITOR_ID`);

--
-- Indexes for table `copy`
--
ALTER TABLE `copy`
  ADD PRIMARY KEY (`DOCID`,`COPYNO`,`LIBID`),
  ADD KEY `COPY_TO_BRANCH` (`LIBID`);

--
-- Indexes for table `document`
--
ALTER TABLE `document`
  ADD PRIMARY KEY (`DOCID`),
  ADD KEY `PUBLISHERID` (`PUBLISHERID`);

--
-- Indexes for table `fine`
--
ALTER TABLE `fine`
  ADD PRIMARY KEY (`READERID`);

--
-- Indexes for table `inv_editor`
--
ALTER TABLE `inv_editor`
  ADD PRIMARY KEY (`DOCID`,`ISSUE_NO`,`IENAME`);

--
-- Indexes for table `journal_issue`
--
ALTER TABLE `journal_issue`
  ADD PRIMARY KEY (`DOCID`,`ISSUE_NO`);

--
-- Indexes for table `journal_volume`
--
ALTER TABLE `journal_volume`
  ADD PRIMARY KEY (`DOCID`),
  ADD KEY `EDITOR_ID` (`EDITOR_ID`);

--
-- Indexes for table `proceedings`
--
ALTER TABLE `proceedings`
  ADD PRIMARY KEY (`DOCID`);

--
-- Indexes for table `publisher`
--
ALTER TABLE `publisher`
  ADD PRIMARY KEY (`PUBLISHERID`);

--
-- Indexes for table `reader`
--
ALTER TABLE `reader`
  ADD PRIMARY KEY (`READERID`);

--
-- Indexes for table `reserves`
--
ALTER TABLE `reserves`
  ADD PRIMARY KEY (`RESNUMBER`),
  ADD KEY `DOCID` (`DOCID`,`COPYNO`,`LIBID`),
  ADD KEY `READERID` (`READERID`);

--
-- Indexes for table `writes`
--
ALTER TABLE `writes`
  ADD PRIMARY KEY (`AUTHORID`,`DOCID`),
  ADD KEY `AUTHORID` (`AUTHORID`),
  ADD KEY `DOCID` (`DOCID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `borrows`
--
ALTER TABLE `borrows`
  MODIFY `BORNUMBER` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `fine`
--
ALTER TABLE `fine`
  MODIFY `READERID` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `reader`
--
ALTER TABLE `reader`
  MODIFY `READERID` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `reserves`
--
ALTER TABLE `reserves`
  MODIFY `RESNUMBER` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `book`
--
ALTER TABLE `book`
  ADD CONSTRAINT `BOOK_TO_DOCUMENT` FOREIGN KEY (`DOCID`) REFERENCES `document` (`DOCID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `borrows`
--
ALTER TABLE `borrows`
  ADD CONSTRAINT `BORROW_TO_COPY` FOREIGN KEY (`DOCID`,`COPYNO`,`LIBID`) REFERENCES `copy` (`DOCID`, `COPYNO`, `LIBID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `BORROW_TO_READER` FOREIGN KEY (`READERID`) REFERENCES `reader` (`READERID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `copy`
--
ALTER TABLE `copy`
  ADD CONSTRAINT `COPY_TO_BRANCH` FOREIGN KEY (`LIBID`) REFERENCES `branch` (`LIBID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `COPY_TO_DOCUMENT` FOREIGN KEY (`DOCID`) REFERENCES `document` (`DOCID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `document`
--
ALTER TABLE `document`
  ADD CONSTRAINT `DOCUMENT_TO_PUBLISHER` FOREIGN KEY (`PUBLISHERID`) REFERENCES `publisher` (`PUBLISHERID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `inv_editor`
--
ALTER TABLE `inv_editor`
  ADD CONSTRAINT `INV_TO_ISSUE` FOREIGN KEY (`DOCID`,`ISSUE_NO`) REFERENCES `journal_issue` (`DOCID`, `ISSUE_NO`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `journal_issue`
--
ALTER TABLE `journal_issue`
  ADD CONSTRAINT `ISSUE_TO_VOLUME` FOREIGN KEY (`DOCID`) REFERENCES `journal_volume` (`DOCID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `journal_volume`
--
ALTER TABLE `journal_volume`
  ADD CONSTRAINT `VOLUME_TO_CHIEF` FOREIGN KEY (`EDITOR_ID`) REFERENCES `chief_editor` (`EDITOR_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `VOLUME_TO_DOCUMENT` FOREIGN KEY (`DOCID`) REFERENCES `document` (`DOCID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `proceedings`
--
ALTER TABLE `proceedings`
  ADD CONSTRAINT `PROCEEDING_TO_DOCUMENT` FOREIGN KEY (`DOCID`) REFERENCES `document` (`DOCID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `reserves`
--
ALTER TABLE `reserves`
  ADD CONSTRAINT `RESERVE_TO_COPY` FOREIGN KEY (`DOCID`,`COPYNO`,`LIBID`) REFERENCES `copy` (`DOCID`, `COPYNO`, `LIBID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `RESERVE_TO_READER` FOREIGN KEY (`READERID`) REFERENCES `reader` (`READERID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `writes`
--
ALTER TABLE `writes`
  ADD CONSTRAINT `WRITES_TO_AUTHOR` FOREIGN KEY (`AUTHORID`) REFERENCES `author` (`AUTHORID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `WRITES_TO_BOOK` FOREIGN KEY (`DOCID`) REFERENCES `book` (`DOCID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
