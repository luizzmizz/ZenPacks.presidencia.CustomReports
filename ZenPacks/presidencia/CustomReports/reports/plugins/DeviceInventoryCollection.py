import logging
log = logging.getLogger("zen.Reports")

from Products.ZenReports import Utils

class DeviceInventoryCollection:
    def run(self, dmd, args):
        report = []

        #the selected devices are all the DeviceClass subdevices
        deviceClass=args.get('DeviceClass','/')
        resultset=set(dmd.Devices.getOrganizer(deviceClass).getSubDevices())-set(dmd.Devices.getOrganizer('/Ignore').getSubDevices())
        group=args.get('groups','/Environment/PRO')
        if group!='/':
          #&ed with the group specification subdevices
          resultset=resultset & set(dmd.Groups.getOrganizer(group).getSubDevices())
        system=args.get('Csystems','/')
        if system!='/':
          #&ed with the system specification subdevices
          resultset=resultset & set(dmd.Systems.getOrganizer(system).getSubDevices())
        location=args.get('location','/Devices')
        if location!='/':
          #&ed with the location specification subdevices
          resultset=resultset & set(dmd.Locations.getOrganizer(location).getSubDevices())
        productionState=args.get('productionState','')

        hwmanufacturer=args.get('HWManufacturer','')
        osmanufacturer=args.get('OSManufacturer','')
        hwproduct=args.get('HWProduct','')
        osproduct=args.get('OSProduct','')
        tOSProductSearch=args.get('tOSProductSearch')
        tHWProductSearch=args.get('tHWProductSearch')

	#devsfiltered contains all HWManuf and OSManuf specification
        devsfiltered=[ i.getObject() for i in dmd.Devices.deviceSearch({'getHWManufacturerName':hwmanufacturer,
                                               'getOSManufacturerName':osmanufacturer}) ]
        #survivordevs are those devices in devsfiltered which matches the hw/os manufacturer/product specifications
        survivordevs=[]
        for dev in devsfiltered:
          valHW=(tHWProductSearch=="1" and hwproduct in dev.getHWProductName() or hwproduct=='____') or (tHWProductSearch!="1" and (hwproduct==dev.getHWProductName() or hwproduct==''))
          valOS=(tOSProductSearch=="1" and osproduct in dev.getOSProductName() or osproduct=='____') or (tOSProductSearch!="1" and (osproduct==dev.getOSProductName() or osproduct==''))
          if valHW and valOS:
             survivordevs.append(dev)

        #for each device at resultset & survivordevs, generate the info
        for dev in resultset & set(survivordevs):
          if (not productionState) or (productionState==dev.getProdState()):
            report.append(
                    Utils.Record(
                      device = dev.name(),
                      deviceLink = dev.getDeviceLink(),
                      manageIp = dev.manageIp,
                      tag = dev.getHWTag,
                      serial = dev.getHWSerialNumber(),
                      deviceClassPath = dev.getDeviceClassPath(),
                      deviceClassPathLink = dev.deviceClass().getIdLink(),
		      productionState = dev.getProdState(),
                      getHW = '%s: %s'%(dev.getHWManufacturerName(),dev.getHWProductName()) ,
                      getHWProductName=dev.getHWProductName(),
                      getHWManufacturerName=dev.getHWManufacturerName(),
                      getOS = '%s: %s'%(dev.getOSManufacturerName(),dev.getOSProductName()) ,
                      getOSProductName=dev.getOSProductName(),
                      getOSManufacturerName=dev.getOSManufacturerName(),
		      location = dev.getLocationName(),
		      locationLink = dev.getLocationLink(),
                      )
                    )
	superreport={}

        superreport['devices']=report
        #osman: get all the OS Manufacturers existing into the resultset devices
        superreport['osman']=sorted(list(set([i.getOSManufacturerName() for i in resultset])))
        #hwman: get all the HW Manufacturers existing itno the resultset devices
        superreport['hwman']=sorted(list(set([i.getHWManufacturerName() for i in resultset])))
        #osproducts: get each of the OSProducts, present into the resultset, related to the selected OSManufacturer (osmanufacturer may be '' for all manufacturers)
        superreport['osproducts']=sorted(list(set([i.getOSProductName() for i in resultset if (i.getOSManufacturerName()==osmanufacturer or osmanufacturer=='')])))
        #hwproducts: get each of the HWProducts, present into the resultset, related to the selected HWManufacturer (hwmanufacturer may be '' for all manufacturers)
        superreport['hwproducts']=sorted(list(set([i.getHWProductName() for i in resultset if (i.getHWManufacturerName()==hwmanufacturer or hwmanufacturer=='')])))
        return superreport
