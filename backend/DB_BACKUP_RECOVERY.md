# Database Backup and Recovery for Todo Application

## Overview
This document outlines the backup and recovery procedures for the Neon PostgreSQL database used in the Todo application.

## Backup Procedures

### Automated Backups
Neon PostgreSQL provides automated backups by default:
- Continuous Protection: Neon continuously backs up your data
- Point-in-Time Recovery: Restore to any point in time within the retention period
- Backup retention: Typically 7 days for free tier, longer for paid tiers

### Manual Backups
To create a manual backup of your database:

1. **Using Neon Console**:
   - Go to your Neon project dashboard
   - Navigate to the "Branches" tab
   - Select your branch and click "..." menu
   - Choose "Restore" to create a new branch from a specific point in time

2. **Using pg_dump** (if needed for external storage):
   ```bash
   pg_dump "postgresql://username:password@hostname:port/database_name" > backup.sql
   ```

## Recovery Procedures

### Restoring from Neon Console
1. Go to your Neon project dashboard
2. Navigate to the "Branches" tab
3. Click "Restore" and select the point in time you want to restore to
4. Choose whether to restore to a new branch or overwrite the current branch

### Application Recovery Steps
1. Ensure the database is restored to the desired state
2. Update the `DATABASE_URL` in your environment variables if needed
3. Restart the application to establish fresh database connections
4. Verify application functionality with the recovered data

## Recovery Time Objectives (RTO)
- Target recovery time: Under 15 minutes for database restoration
- Application restart time: Under 5 minutes

## Recovery Point Objectives (RPO)
- Data loss tolerance: Maximum 1 hour of data (depending on Neon's backup frequency)
- For critical operations, consider more frequent manual backups

## Monitoring and Verification

### Backup Verification
- Regularly check that automated backups are occurring
- Test restore procedures periodically to ensure backups are valid
- Monitor disk space usage to ensure sufficient space for backups

### Recovery Testing
- Periodically test the recovery process in a non-production environment
- Verify data integrity after recovery
- Test application functionality with recovered data

## Security Considerations
- Database credentials should never be stored in backup files if using external tools
- Ensure encrypted transmission of backup data when transferring
- Limit access to backup files to authorized personnel only

## Contact Information
- For Neon-specific issues: Contact Neon support through the console
- For application-specific issues: Contact the development team

## Emergency Procedures
In case of database failure:
1. Assess the scope of the issue
2. Check Neon status page for any ongoing incidents
3. Initiate recovery procedure based on the last known good backup
4. Notify stakeholders of the incident and estimated recovery time
5. Document the incident and recovery process for future reference