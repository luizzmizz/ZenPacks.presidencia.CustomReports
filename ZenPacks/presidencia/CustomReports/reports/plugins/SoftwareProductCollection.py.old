import logging
log = logging.getLogger("zen.Reports")

from Products.ZenReports import Utils

class SoftwareProductCollection:
    def run(self, dmd, args):
        report = []

        deviceClass=args.get('DeviceClass','/Server')
        resultset=set(dmd.Devices.getOrganizer(deviceClass).getSubDevices())-set(dmd.Devices.getOrganizer('/Ignore').getSubDevices())
        group=args.get('groups','/Environment/PRO')
        if group!='/':
          resultset=resultset & set(dmd.Groups.getOrganizer(group).getSubDevices())
        system=args.get('Csystems','/')
        if system!='/':
          resultset=resultset & set(dmd.Systems.getOrganizer(system).getSubDevices())
        location=args.get('location','/Devices')
        if location!='/':
          resultset=resultset & set(dmd.Locations.getOrganizer(location).getSubDevices())
        productionState=args.get('productionState','')

        for dev in list(resultset):
          if (not productionState) or (productionState==dev.getProdState()):
            report.append(
                    Utils.Record(
                      device = dev.name(),
                      deviceLink = dev.getDeviceLink(),
                      manageIp = dev.manageIp,
                      tag = dev.getHWTag,
                      deviceClassPath = '.%s'%dev.getDeviceClassPath().replace(deviceClass,'',1),
                      deviceClassPathLink = dmd.Devices.getOrganizer(dev.getDeviceClassPath()).getIdLink(),
		      productionState = dev.getProdState(),
                      getHW = '%s: %s'%(dev.getHWManufacturerName(),dev.getHWProductName()) ,
                      getOS = '%s: %s'%(dev.getOSManufacturerName(),dev.getOSProductName()) ,
		      location = dev.getLocationName().replace(location,'',1),
                      )
                    )
        superreport={dd}
        superreport['devices']=report
        superreport['osmanuf']=list(set([i.getObject().getManufacturerName() for i in dmd.Manufacturers.productSearch({'meta_type':'SoftwareClass','isOS':True})]))
        superreport['hwmanuf']=list(set([i.getObject().getManufacturerName() for i in dmd.Manufacturers.productSearch({'meta_type':'HardwareClass'})]))
        return report
