/**
 * HomeLab OS Frontend SDK
 *
 * Exposes a unified client SDK for all platform features, isolating
 * frontend components from raw HTTP fetch / axios clients.
 */

import AuthSDK from './AuthSDK';
import SystemSDK from './SystemSDK';
import StorageSDK from './StorageSDK';
import VaultSDK from './VaultSDK';
import ProjectsSDK from './ProjectsSDK';
import WorkspaceSDK from './WorkspaceSDK';
import { MonitoringSDK } from './MonitoringSDK';

import NotificationsSDK from './NotificationsSDK';
import SnapshotSDK from './SnapshotSDK';
import BackupSDK from './BackupSDK';
import DocumentationSDK from './DocumentationSDK';
import DownloadSDK from './DownloadSDK';
import { RemoteSDK } from './RemoteSDK';
import { NetworkSDK } from './NetworkSDK';
import { DevicesSDK } from './DevicesSDK';
import { PluginsSDK } from './PluginsSDK';
import { ActivitySDK } from './ActivitySDK';
import { SettingsSDK } from './SettingsSDK';
import { HealthSDK } from './HealthSDK';
import { JobsSDK } from './JobsSDK';
import { TransfersSDK } from './TransfersSDK';

class HomeLabSDK {
  constructor(apiClient) {
    this.auth = new AuthSDK(apiClient);
    this.system = new SystemSDK(apiClient);
    this.storage = new StorageSDK(apiClient);
    this.vault = new VaultSDK(apiClient);
    this.projects = new ProjectsSDK(apiClient);
    this.workspace = new WorkspaceSDK(apiClient);
    this.monitoring = new MonitoringSDK(apiClient);
    this.notifications = new NotificationsSDK(apiClient);
    this.snapshots = new SnapshotSDK(apiClient);
    this.backup = new BackupSDK(apiClient);
    this.documentation = new DocumentationSDK(apiClient);
    this.downloads = new DownloadSDK(apiClient);
    this.remote = RemoteSDK;
    this.network = NetworkSDK;
    this.devices = DevicesSDK;
    this.plugins = PluginsSDK;
    this.activity = ActivitySDK;
    this.settings = SettingsSDK;
    this.health = HealthSDK;
    this.jobs = JobsSDK;
    this.transfers = TransfersSDK;
  }
}

export default HomeLabSDK;
export {
  AuthSDK,
  SystemSDK,
  StorageSDK,
  VaultSDK,
  ProjectsSDK,
  WorkspaceSDK,
  MonitoringSDK,
  NotificationsSDK,
  SnapshotSDK,
  BackupSDK,
  DocumentationSDK,
  DownloadSDK,
  RemoteSDK,
  NetworkSDK,
  DevicesSDK,
  PluginsSDK,
  ActivitySDK,
  SettingsSDK,
  HealthSDK,
  JobsSDK,
  TransfersSDK,
};




