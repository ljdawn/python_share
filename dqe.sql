CREATE PROCEDURE `dist_queue_email`(IN in_pubid INT BIGINT)
sproc:BEGIN

DECLARE v_org_pub_id INT UNSIGNED;

DROP TABLE IF EXISTS smsdb.email_details_temp; 
CREATE TEMPORARY TABLE IF NOT EXISTS smsdb.email_details_temp LIKE smsdb.email_details;

SELECT COALESCE(pub.org_pub_id, pub.id)
  INTO v_org_pub_id
  FROM nisdb.pubs_publication pub
 WHERE pub.id = in_pubid;
       

INSERT IGNORE INTO email_details_temp 
       (pub_id, sub_id, create_time, full_name, address, status, attempts, org_pub_id)
SELECT pub_id, sub_id, now(), sub_full_name, sub_email, 0, 0, v_org_pub_id
  FROM dist_subscriptions
 WHERE pub_id = in_pubid
   AND status = 0
   AND send_email = 1;

UPDATE email_details_temp e, nixle.nixle_profile p, nixle.auth_user u
   SET e.language = p.language
 WHERE p.language NOT IN ('en', 'en-US')
   AND p.user_id = u.id
   AND u.email = e.address;

INSERT IGNORE INTO smsdb.email_details
SELECT * 
  FROM smsdb.email_details_temp;

END
