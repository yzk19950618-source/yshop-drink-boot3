package co.yixiang.yshop.module.order.service.storeordercartinfo;

import cn.hutool.core.util.IdUtil;
import cn.hutool.core.util.StrUtil;
import co.yixiang.yshop.module.order.dal.dataobject.storeordercartinfo.StoreOrderCartInfoDO;
import co.yixiang.yshop.module.order.dal.mysql.storeordercartinfo.StoreOrderCartInfoMapper;
import co.yixiang.yshop.module.product.dal.dataobject.storeproduct.StoreProductDO;
import co.yixiang.yshop.module.product.dal.dataobject.storeproductattrvalue.StoreProductAttrValueDO;
import co.yixiang.yshop.module.product.service.storeproduct.AppStoreProductService;
import co.yixiang.yshop.module.product.service.storeproductattrvalue.StoreProductAttrValueService;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.toolkit.Wrappers;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import jakarta.annotation.Resource;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.validation.annotation.Validated;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

/**
 * 订单购物详情 Service 实现类
 *
 * @author yshop
 */
@Slf4j
@Service
@Validated
public class StoreOrderCartInfoServiceImpl extends ServiceImpl<StoreOrderCartInfoMapper, StoreOrderCartInfoDO> implements StoreOrderCartInfoService {

    @Resource
    private AppStoreProductService appStoreProductService;
    @Resource
    private StoreProductAttrValueService storeProductAttrValueService;


    /**
     * 添加购物车商品信息
     * @param oid 订单id
     * @param orderId
     * @param productIds 商品id
     * @param numbers 商品数量
     * @param specs 商品规格
     */
    @Override
    public void saveCartInfo(Long oid, String orderId, List<String> productIds, List<String> numbers,
                             List<String> specs, List<String> specAddons) {
        log.info("==========添加购物车商品信息start===========");

        List<StoreOrderCartInfoDO> list = new ArrayList<>();
        for (int i = 0; i < productIds.size(); i++) {
            String newSku = StrUtil.replace(specs.get(i), "|", ",");
            StoreProductDO storeProductDO = appStoreProductService.getById(productIds.get(i));
            if (storeProductDO == null) {
                log.error("[saveCartInfo][商品不存在 productId={}]", productIds.get(i));
                continue;
            }

            StoreProductAttrValueDO storeProductAttrValue = storeProductAttrValueService
                    .getOne(Wrappers.<StoreProductAttrValueDO>lambdaQuery()
                            .eq(StoreProductAttrValueDO::getSku, newSku)
                            .eq(StoreProductAttrValueDO::getProductId, productIds.get(i)));
            BigDecimal linePrice = storeProductAttrValue != null ? storeProductAttrValue.getPrice()
                    : storeProductDO.getPrice();
            if (storeProductAttrValue == null) {
                log.warn("[saveCartInfo][未匹配 SKU，使用商品原价 oid={} productId={} sku={}]",
                        oid, productIds.get(i), newSku);
            }
            if (linePrice == null) {
                linePrice = BigDecimal.ZERO;
            }

            StoreOrderCartInfoDO info = new StoreOrderCartInfoDO();
            info.setOid(oid);
            info.setOrderId(orderId);
            info.setCartId(0L);
            info.setProductId(Long.valueOf(productIds.get(i)));
            info.setCartInfo("");
            info.setUnique(IdUtil.simpleUUID());
            info.setIsAfterSales(1);
            info.setTitle(storeProductDO.getStoreName());
            info.setImage(storeProductDO.getImage());
            info.setNumber(Integer.valueOf(numbers.get(i)));
            String displaySpec = specs.get(i);
            if (specAddons != null && i < specAddons.size()) {
                String addon = specAddons.get(i);
                if (StrUtil.isNotBlank(addon)) {
                    displaySpec = displaySpec + " | " + addon;
                }
            }
            info.setSpec(displaySpec);
            info.setPrice(linePrice);
            list.add(info);

        }

        if (!list.isEmpty()) {
            this.saveBatch(list);
        }
    }



}
