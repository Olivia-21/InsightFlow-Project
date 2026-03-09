package com.insightflow.service;

import java.math.BigDecimal;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;

import com.insightflow.dto.ProductSummaryDto;
import com.insightflow.mapper.ProductMapper;
import com.insightflow.model.Product;
import com.insightflow.repository.ProductRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class ProductService {

    private final ProductRepository productRepository;
    private final ProductMapper productMapper;

    public List<ProductSummaryDto> findAll() {
        return productRepository.findAll().stream()
                .map(productMapper::toSummaryDto)
                .collect(Collectors.toList());
    }

    public ProductSummaryDto findById(Integer id) {
        Product product = productRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Product not found with id: " + id));
        return productMapper.toSummaryDto(product);
    }

    public List<ProductSummaryDto> searchByName(String name) {
        return productRepository.searchByName(name).stream()
                .map(productMapper::toSummaryDto)
                .collect(Collectors.toList());
    }

    public List<ProductSummaryDto> findByStoreId(Integer storeId) {
        return productRepository.findByStoreStoreId(storeId).stream()
                .map(productMapper::toSummaryDto)
                .collect(Collectors.toList());
    }

    public List<ProductSummaryDto> findByCategoryId(Integer categoryId) {
        return productRepository.findByCategoryCategoryId(categoryId).stream()
                .map(productMapper::toSummaryDto)
                .collect(Collectors.toList());
    }

    public List<ProductSummaryDto> findByPriceRange(BigDecimal minPrice, BigDecimal maxPrice) {
        return productRepository.findByPriceRange(minPrice, maxPrice).stream()
                .map(productMapper::toSummaryDto)
                .collect(Collectors.toList());
    }

    public List<ProductSummaryDto> findByMaxPrice(BigDecimal maxPrice) {
        return productRepository.findByPriceLessThanOrEqual(maxPrice).stream()
                .map(productMapper::toSummaryDto)
                .collect(Collectors.toList());
    }

    public ProductSummaryDto create(ProductSummaryDto dto) {
        Product product = productMapper.toEntity(dto);
        return productMapper.toSummaryDto(productRepository.save(product));
    }

    public ProductSummaryDto update(Integer id, ProductSummaryDto dto) {
        Product product = productRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Product not found with id: " + id));

        product.setProductName(dto.getName());
        product.setDescription(dto.getDescription());
        product.setUnitPrice(dto.getPrice());

        return productMapper.toSummaryDto(productRepository.save(product));
    }

    public void delete(Integer id) {
        if (!productRepository.existsById(id)) {
            throw new RuntimeException("Product not found with id: " + id);
        }
        productRepository.deleteById(id);
    }
}
