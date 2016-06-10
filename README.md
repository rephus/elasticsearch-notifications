## Description

Get email notifications when some `data` is available on Elastic Search

E.g: Get reports for some users who accessed the site in the last 24h.

## ES Filtering

By default, this script is making a query to ES with a time filter (specified in config),
and group users by their `email`.

Adapt this query to your needs.

## Config

This script is using gmail to send emails, setup your config credentials on `config.cfg`
(see config.cfg.sample for more details).

Feel free to setup your own email delivery service (mandrill, mailGun, sendInBlue...) or
your own message service (slack, pushBullet...)

## Crontab

You can run this script on a cronjob periodically.

E.g: To run every 24h

    0 0 * * * cd elasticsearch-notifications && python run.py >> output.log 2>&1
