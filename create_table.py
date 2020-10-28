'''
CREATE TABLE `z_api_saramin` (
	`id` CHAR(9) NOT NULL DEFAULT '' COMMENT 'The unique identifier for a job.' COLLATE 'utf8mb4_general_ci',
	`url` VARCHAR(255) NULL COMMENT '채용공고 표준 URL. 공채속보의 경우, 리디렉션이 있을 수 있습니다.' COLLATE 'utf8mb4_general_ci',
	`active` VARCHAR(255) NULL COMMENT '공고 진행 여부' COLLATE 'utf8mb4_general_ci',
	`posting-timestamp` VARCHAR(255) NULL COMMENT '게시일의 Unix timestamp' COLLATE 'utf8mb4_general_ci',
	`posting-date` VARCHAR(255) NULL COMMENT '날짜/시간 형식의 게시일 (2019-07-07T17:17:17+0900)' COLLATE 'utf8mb4_general_ci',
	`modification-timestamp` VARCHAR(255) NULL COMMENT '수정일 Unix timestamp' COLLATE 'utf8mb4_general_ci',
	`opening-timestamp` VARCHAR(255) NULL COMMENT '접수 시작일의 Unix timestamp' COLLATE 'utf8mb4_general_ci',
	`expiration-timestamp` VARCHAR(255) NULL COMMENT '마감일의 Unix timestamp' COLLATE 'utf8mb4_general_ci',
	`expiration-date` VARCHAR(255) NULL COMMENT '날짜/시간 형식의 마감일' COLLATE 'utf8mb4_general_ci',
	`read-cnt` VARCHAR(255) NULL COMMENT '조회수' COLLATE 'utf8mb4_general_ci',
	`apply-cnt` VARCHAR(255) NULL COMMENT '지원자수' COLLATE 'utf8mb4_general_ci',
	`keyword` TEXT NULL COMMENT '키워드 (쉼표로 구분됨)' COLLATE 'utf8mb4_general_ci',
	`close-type_code` VARCHAR(255) NULL COMMENT '마감일 형식' COLLATE 'utf8mb4_general_ci',
	`close-type_Text` VARCHAR(255) NULL COMMENT '마감일 형식' COLLATE 'utf8mb4_general_ci',
	`href` VARCHAR(255) NULL COMMENT '기업정보 페이지(공개되어 있는 경우)' COLLATE 'utf8mb4_general_ci',
	`name_Text` VARCHAR(255) NULL COMMENT '기업명' COLLATE 'utf8mb4_general_ci',
	`title` VARCHAR(255) NULL COMMENT '공고 제목' COLLATE 'utf8mb4_general_ci',
	`location_code` VARCHAR(255) NULL COMMENT '지역 (@code: 지역코드)' COLLATE 'utf8mb4_general_ci',
	`location_Text` TEXT NULL COMMENT '지역 (@code: 지역코드)' COLLATE 'utf8mb4_general_ci',
	`job-type_code` VARCHAR(255) NULL COMMENT '근무형태 (@code, 쉼표/comma로 구분됨, 근무형태코드 참고)' COLLATE 'utf8mb4_general_ci',
	`job-type_Text` VARCHAR(255) NULL COMMENT '근무형태 (@code, 쉼표/comma로 구분됨, 근무형태코드 참고)' COLLATE 'utf8mb4_general_ci',
	`industry_code` VARCHAR(255) NULL COMMENT '업종 (@code, 쉼표로 구분됨) 업종 코드표 참고' COLLATE 'utf8mb4_general_ci',
	`industry_Text` TEXT NULL COMMENT '업종 (@code, 쉼표로 구분됨) 업종 코드표 참고' COLLATE 'utf8mb4_general_ci',
	`job-category_code` VARCHAR(255) NULL COMMENT '직종 (@code, 쉼표로 구분됨) 직종 코드표 참고' COLLATE 'utf8mb4_general_ci',
	`job-category_Text` TEXT NULL COMMENT '직종 (@code, 쉼표로 구분됨) 직종 코드표 참고' COLLATE 'utf8mb4_general_ci',
	`industry-keyword-code` TEXT NULL COMMENT '업종 키워드 코드 (@code, 쉼표로 구분됨) 업종 키워드 코드표 참고' COLLATE 'utf8mb4_general_ci',
	`job-category-keyword-code` TEXT NULL COMMENT '직종 키워드 (@code, 쉼표로 구분됨) 직종 키워드 코드표 참고' COLLATE 'utf8mb4_general_ci',
	`experience-level_code` VARCHAR(255) NULL COMMENT '경력 (@min: 최소경력, @max: 최대경력)' COLLATE 'utf8mb4_general_ci',
	`min` VARCHAR(255) NULL COMMENT '경력 (@min: 최소경력, @max: 최대경력)' COLLATE 'utf8mb4_general_ci',
	`max` VARCHAR(255) NULL COMMENT '경력 (@min: 최소경력, @max: 최대경력)' COLLATE 'utf8mb4_general_ci',
	`experience-level_Text` VARCHAR(255) NULL COMMENT '경력 (@min: 최소경력, @max: 최대경력)' COLLATE 'utf8mb4_general_ci',
	`required-education-level_code` VARCHAR(255) NULL COMMENT '학력, 학력 코드표 참고' COLLATE 'utf8mb4_general_ci',
	`required-education-level_Text` VARCHAR(255) NULL COMMENT '학력, 학력 코드표 참고' COLLATE 'utf8mb4_general_ci',
	`salary_code` VARCHAR(255) NULL COMMENT '연봉 (@code) 연봉 범위 코드표 참고' COLLATE 'utf8mb4_general_ci',
	`salary_Text` TEXT NULL COMMENT '연봉 (@code) 연봉 범위 코드표 참고' COLLATE 'utf8mb4_general_ci',
	`bizNum` CHAR(10) NULL COLLATE 'utf8mb4_general_ci',
	`getDate` VARCHAR(50) NULL COLLATE 'utf8mb4_general_ci',
	`crawlExist` CHAR(1) NULL DEFAULT '' COMMENT '0=not crawl, 1=crawl' COLLATE 'utf8mb4_general_ci',
	`crawlCompanyLogo` LONGTEXT NULL COLLATE 'utf8mb4_general_ci',
	`crawlSummary` LONGTEXT NULL COLLATE 'utf8mb4_general_ci',
	`crawlDetail` LONGTEXT NULL COLLATE 'utf8mb4_general_ci',
	`crawlDeadline` LONGTEXT NULL COLLATE 'utf8mb4_general_ci',
	`crawlCompany` LONGTEXT NULL COLLATE 'utf8mb4_general_ci',
	`iframe` LONGTEXT NULL COLLATE 'utf8mb4_general_ci',
	`middleAge` CHAR(1) NULL DEFAULT '0' COMMENT '0=중장년 아님, 1=중장년' COLLATE 'utf8mb4_general_ci',
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `getDate` (`getDate`) USING BTREE,
	INDEX `crawlExist` (`crawlExist`) USING BTREE,
	INDEX `deadline` (`expiration-date`(191)) USING BTREE,
	INDEX `opening` (`opening-timestamp`(191)) USING BTREE,
	FULLTEXT INDEX `texts` (`keyword`, `title`, `crawlSummary`, `crawlDetail`),
	FULLTEXT INDEX `iframe` (`iframe`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;
'''