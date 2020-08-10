module.exports = {
    apps : [{
      name: 'Corretoras Scraping',
      cmd: '/media/laura/dados/Projects/Work/searchKeyword/scripts/main.py',
      interpreter: 'python3',
      args: '',
      instances: 1,
      autorestart: true,
      watch: true,
      max_memory_restart: '8G',
      env: {
        NODE_ENV: 'development'
      },
      env_production: {
        NODE_ENV: 'production'
      }
    }]
  };
  
  