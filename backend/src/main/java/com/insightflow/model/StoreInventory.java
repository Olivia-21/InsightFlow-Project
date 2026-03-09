package com.insightflow.model;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDate;

@Entity
@Table(name = "storeinventory", uniqueConstraints = {
        @UniqueConstraint(columnNames = { "store_id", "product_id" }, name = "uk_store_inventory")
})
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class StoreInventory {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "store_inventory_id")
    private Integer storeInventoryId;

    @Column(name = "opening_stock")
    private Integer openingStock;

    @Column(name = "closing_stock", nullable = false)
    private Integer closingStock;

    @Column(name = "unit_received")
    private Integer unitReceived;

    @Column(name = "unit_sold")
    private Integer unitSold;

    @Column(name = "needs_reorder")
    private Boolean needsReorder;

    @UpdateTimestamp
    @Column(name = "stock_date", nullable = false, columnDefinition = "DATE DEFAULT CURRENT_DATE")
    private LocalDate stockDate;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "store_id", nullable = false, foreignKey = @ForeignKey(name = "fk_store_inventory_store_id"))
    private Store store;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "product_id", nullable = false, foreignKey = @ForeignKey(name = "fk_store_inventory_product_id"))
    private Product product;
}