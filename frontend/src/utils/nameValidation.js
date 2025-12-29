function isAlphanumeric(str) {
    return /^[a-z0-9 ]+$/i.test(str);
}
export function nameSeperate(str) {
    const ret = {};
    if (str.includes("#")) {
        const splitName = str.split("#");
        ret.name = splitName[0];
        ret.tag = splitName[1];
        if (isAlphanumeric(ret.name) && isAlphanumeric(ret.tag)) {
            ret.error = false;
            return ret;
        }
    }
    return { error: true };
}

export function getMainPlatform(region) {
  const mapping = {
    'americas': 'na1',
    'europe': 'euw1',
    'asia': 'kr',
    'sea': 'oc1'
  };
  return mapping[region.toLowerCase()];
}
