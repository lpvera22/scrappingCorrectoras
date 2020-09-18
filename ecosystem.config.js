module.exports = {
  apps : [{
    name: 'backend',
    cmd: '/root/projects/scrappingCorrectoras/wsgi.py',
    interpreter: 'python3',
    args: '',
    instances: 1,
    autorestart: true,
    watch: true,
    // max_memory_restart: '1G',s
    env: {
      NODE_ENV: 'development'
    },
    env_production: {
      NODE_ENV: 'production'
    }
  }]
 };
