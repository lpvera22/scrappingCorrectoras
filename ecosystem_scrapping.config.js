module.exports = {
    apps : [{
      name: 'scrapping',
      script: '/root/projects/scrappingCorrectoras/scripts/main.py',
      interpreter: '/usr/bin/python3',
      instances: 1,
      autorestart: false,
      watch: false, 
      cron_restart:'0 */12 * * *'
    }]
   };